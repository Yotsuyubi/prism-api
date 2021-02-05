from demucs.utils import load_model, apply_model
from demucs.audio import AudioFile
from io import BytesIO
from scipy.io import wavfile
import zipfile
import os
import tempfile


class Separater(object):

    def __init__(self):
        self.model = None

    def load_model(self, path='models/model.th.gz'):
        if self.model is None:
            self.model = load_model(path)
            return True
        else:
            return False

    def __call__(self, buffer=None, path=None):

        if buffer is not None:
            with tempfile.NamedTemporaryFile(suffix='.wav', prefix=os.path.basename(__file__)) as out:
                out.write(buffer.read())
                mix_buf.close()
                wav = AudioFile(out.name).read(streams=0, samplerate=44100, channels=2).to('cpu')

        else:
            wav = AudioFile(path).read(streams=0, samplerate=44100, channels=2).to('cpu')

        wav = (wav * 2**15).round() / 2**15
        ref = wav.mean(0)
        wav = (wav - ref.mean()) / ref.std()
        sources = apply_model(self.model, wav, shifts=0, split=True)
        sources = sources * ref.std() + ref.mean()

        buffers = []
        for source in sources:
            source = source.cpu().transpose(0, 1).numpy()
            buf = BytesIO()
            wavfile.write(buf, 44100, source)
            buffers.append(buf)

        zip_buffer = self.make_zip(buffers)

        return zip_buffer

    def make_zip(self, buffers):
        zip_buffer = BytesIO()
        name = ["drums.wav", "bass.wav", "other.wav", "vocals.wav"]

        with zipfile.ZipFile(zip_buffer, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
            for buffer, name in zip(buffers, name):
                new_zip.writestr(name, buffer.getvalue())
                buffer.close()

        return zip_buffer
