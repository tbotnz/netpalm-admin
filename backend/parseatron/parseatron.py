import textfsm
from ttp import ttp
from backend.confload.confload import Config
import uuid
import os


class ParseAtron:
    def __init__(self):
        self.config = Config()

    def parsefsm(self, cli_txt=None, fsm_template=None):
        # note to self, fix this
        fsm_fn_fp = "backend/temp_fs/fsm"+str(uuid.uuid4())
        cli_fn_fp = "backend/temp_fs/cli"+str(uuid.uuid4())

        cli_file = open(cli_fn_fp, "w")
        n = cli_file.write(cli_txt)
        cli_file.close()

        fsm_file = open(fsm_fn_fp, "w")
        n = fsm_file.write(fsm_template)
        fsm_file.close()

        input_file = open(cli_fn_fp, encoding='utf-8')
        raw_text_data = input_file.read()
        input_file.close()

        try:
            template = open(fsm_fn_fp,)
            re_table = textfsm.TextFSM(template)
            fsm_results = re_table.ParseText(raw_text_data)
            result_list = [dict(zip(re_table.header, pr)) for pr in fsm_results]
            template.close()
            os.remove(fsm_fn_fp)
            os.remove(cli_fn_fp)
            return result_list
        except Exception as e:
            fsm_file.close()
            os.remove(fsm_fn_fp)
            os.remove(cli_fn_fp)
            return [str(e)]

    def parsettp(self, cli_txt=None, fsm_template=None):
        fsm_fn_fp = "backend/temp_fs/fsm"+str(uuid.uuid4())
        cli_fn_fp = "backend/temp_fs/cli"+str(uuid.uuid4())

        cli_file = open(cli_fn_fp, "w")
        n = cli_file.write(cli_txt)
        cli_file.close()

        fsm_file = open(fsm_fn_fp, "w")
        n = fsm_file.write(fsm_template)
        fsm_file.close()

        try:
            # read files
            input_file = open(cli_fn_fp, encoding='utf-8')
            raw_text_data = input_file.read()
            input_file.close()

            parser = ttp(data=raw_text_data, template=fsm_fn_fp)
            parser.parse()
            results = parser.result(format='raw')
            return results
        except Exception as e:
            os.remove(fsm_fn_fp)
            os.remove(cli_fn_fp)
            return str(e)
