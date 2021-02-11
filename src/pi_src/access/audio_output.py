# dateコマンドを実行して文字列として結果を得る
import subprocess
from subprocess import PIPE


class audio_output():
    def user_scream(self, user_name):
        proc = subprocess.run('~/RAS_src/aquestalkpi/AquesTalkPi "{0}" | aplay'.format(user_name), 
            shell=True, stdout=PIPE, stderr=PIPE, text=True)

if __name__ == "__main__":
    ao = audio_output()
    ao.user_scream("tamakawa") 