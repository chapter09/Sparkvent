import time
from multiprocessing import Process

from http_req import *
from url_gen import *
from resp_parse import *


# need to make a thread to query periodically
class Client(object):

    def __init__(self, config):
        self.config = config
        self.url_gen = UrlGen()
        self.requester = HttpRequester()
        self.app_parser = AppParser()
        self.job_parser = JobParser()
        self.stage_parser = StageParser()

    # get all available info (apps, jobs, stages)
    def get_all_info(self):
        data = []
        entry = {'application': None, 'jobs': None, 'stages': None}
        apps = self.get_all_applications()
        for app in apps:
            entry['application'] = app
            entry['jobs'] = self.get_all_jobs_from_application(app.id)
            entry['stages'] = self.get_all_stages_from_application(app.id)
            data.append(entry)
        return data

    def get_all_applications(self):
        rest_api = ''
        data = self._get_data(rest_api, self.app_parser)
        return data

    def get_all_jobs_from_application(self, app_id):
        rest_api = app_id + '/' + 'jobs'
        data = self._get_data(rest_api, self.job_parser)
        return data

    def get_job_from_application(self, app_id, job_id):
        rest_api = app_id + '/' + 'jobs' + '/' + job_id
        data = self._get_data(rest_api, self.job_parser)
        return data

    def get_all_stages_from_application(self, app_id):
        rest_api = app_id + '/' + 'stages'
        data = self._get_data(rest_api, self.stage_parser)
        return data

    def get_stage_from_application(self, app_id, stage_id):
        rest_api = app_id + '/' + 'stages' + '/' + stage_id
        data = self._get_data(rest_api, self.stage_parser)
        return data

    def _get_data(self, rest_api, parser):
        url = self.url_gen.get_url(self.config.history_server, rest_api)
        json_response = self.requester.single_request(url)

        #response = parser.parse_json(json_response)
        #return response
        return json_response

    def store_info(self, ):
        pass

    def run_daemon(self):
        process = Process(target=self._daemon_process())
        process.start()
        process.join()

    def _daemon_process(self):
        while True:
            data = self.get_all_applications()
            print data
            time.sleep(self.config.period)
