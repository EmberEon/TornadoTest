from alibabacloud_imageaudit20191230 import models as imageaudit_20191230_models
from alibabacloud_sample.sample import Sample
from configs.config import ali_yun_conf
from forum.handler.BaseHandler import BaseHandler
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class AliYunApi(BaseHandler):

    def __init__(self):
        self.__client = Sample.create_client(ali_yun_conf.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
                                             ali_yun_conf.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET'))
        labels_0 = imageaudit_20191230_models.ScanTextRequestLabels(
            label='spam'
        )
        labels_1 = imageaudit_20191230_models.ScanTextRequestLabels(
            label='politics'
        )
        labels_2 = imageaudit_20191230_models.ScanTextRequestLabels(
            label='abuse'
        )
        labels_3 = imageaudit_20191230_models.ScanTextRequestLabels(
            label='terrorism'
        )
        labels_4 = imageaudit_20191230_models.ScanTextRequestLabels(
            label='porn'
        )
        labels_5 = imageaudit_20191230_models.ScanTextRequestLabels(
            label='flood'
        )
        labels_6 = imageaudit_20191230_models.ScanTextRequestLabels(
            label='contraband'
        )
        labels_7 = imageaudit_20191230_models.ScanTextRequestLabels(
            label='ad'
        )
        self.__labels = [labels_0, labels_1, labels_2, labels_3, labels_4, labels_5, labels_6, labels_7]
        self.__runtime = util_models.RuntimeOptions()

    async def check_txt(self):
        tasks_0 = imageaudit_20191230_models.ScanTextRequestTasks(
            content='本校小额贷款，安全、快捷、方便、无抵押，随机随贷，当天放款，上门服务。联系weixin 123456')
        scan_text_request = imageaudit_20191230_models.ScanTextRequest(tasks=[tasks_0], labels=self.__labels)
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = self.__client.scan_text_with_options(scan_text_request, self.__runtime)
            dict = response.body.to_map()
            return dict
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error)
