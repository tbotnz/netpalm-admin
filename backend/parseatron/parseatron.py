import textfsm
from ttp import ttp
from jinja2 import Environment, FileSystemLoader

import uuid
import os
import json

from backend.confload.confload import Config


class ParseAtron:
    def __init__(self):
        self.config = Config()

    def generate_temp_fn(self):
        fp = "backend/temp_fs/"+str(uuid.uuid4())
        return fp

    def write_temp_file(self, file_payload):
        file_path = self.generate_temp_fn()
        temp_file = open(file_path, "w")
        temp_file.write(file_payload)
        temp_file.close()
        return file_path

    def cleanup_temp_files(self, file_one=None, file_two=None):
        if file_one:
            os.remove(file_one)
        if file_two:
            os.remove(file_two)

    def parsefsm(self, cli_txt=None, fsm_template=None):
        cli_fn_fp = self.write_temp_file(file_payload=cli_txt)
        fsm_fn_fp = self.write_temp_file(file_payload=fsm_template)

        input_file = open(cli_fn_fp, encoding='utf-8')
        raw_text_data = input_file.read()
        input_file.close()

        try:
            template = open(fsm_fn_fp,)
            re_table = textfsm.TextFSM(template)
            fsm_results = re_table.ParseText(raw_text_data)
            result_list = [dict(zip(re_table.header, pr)) for pr in fsm_results]
            template.close()
            self.cleanup_temp_files(file_one=fsm_fn_fp, file_two=cli_fn_fp)
            return result_list
        except Exception as e:
            template.close()
            self.cleanup_temp_files(file_one=fsm_fn_fp, file_two=cli_fn_fp)
            return [str(e)]

    def parsettp(self, cli_txt=None, fsm_template=None):
        cli_fn_fp = self.write_temp_file(file_payload=cli_txt)
        fsm_fn_fp = self.write_temp_file(file_payload=fsm_template)

        try:
            # read files
            input_file = open(cli_fn_fp, encoding='utf-8')
            raw_text_data = input_file.read()
            input_file.close()

            parser = ttp(data=raw_text_data, template=fsm_fn_fp)
            parser.parse()
            results = parser.result(format='raw')
            self.cleanup_temp_files(file_one=fsm_fn_fp, file_two=cli_fn_fp)
            return results
        except Exception as e:
            self.cleanup_temp_files(file_one=fsm_fn_fp, file_two=cli_fn_fp)
            return str(e)

    def parsej2(self, cli_txt=None, fsm_template=None):
        fsm_fn_fp = self.write_temp_file(file_payload=fsm_template)

        try:
            j2_file_loader = FileSystemLoader("backend/temp_fs/")
            j2_env = Environment(
                                loader=j2_file_loader,
                                lstrip_blocks=True,
                                trim_blocks=True
                                )
            template = j2_env.get_template(fsm_fn_fp.replace("backend/temp_fs/", ""))
            cli_dict = json.loads(cli_txt)
            res = template.render(cli_dict)
            self.cleanup_temp_files(file_one=fsm_fn_fp)
            return [res]
        except Exception as e:
            self.cleanup_temp_files(file_one=fsm_fn_fp)
            return str(e)
