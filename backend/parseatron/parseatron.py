import textfsm
import ttp
from backend.confload.confload import Config
import uuid

class ParseAtron:
    def __init__(self):
        self.config = Config()

    def parsefsm(self, cli_txt=None, fsm_template=None):
        # try:
        #     fsm_tmp_fn = str(uuid.uuid4())
        #     cli_tmp_fn = str(uuid.uuid4())
        #     fsm_fh = open(fsm_tmp_fn, "w")
        #     fsm_fh_ = fsm_fh.write(fsm_template)
        #     fsm_fh.close()
        #     cli_fh = open(cli_tmp_fn, "w")
        #     cli_fh_ = cli_fh.write(cli_txt)
        #     cli_fh.close()
        #     re_table = textfsm.TextFSM(fsm_fh)
        #     fsm_results = re_table.ParseText(cli_fh)
        #     result_list = [dict(zip(re_table.header, pr)) for pr in fsm_results]
        #     fsm_fh.close()
        #     cli_fh.close()
        #     return result_list
        # except Exception as e:
        #     fsm_fh.close()
        #     cli_fh.close()
        #     return [str(e)]
        return True