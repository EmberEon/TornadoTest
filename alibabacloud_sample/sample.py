# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys

from typing import List

from alibabacloud_imageaudit20191230.client import Client as imageaudit20191230Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_imageaudit20191230 import models as imageaudit_20191230_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> imageaudit20191230Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # Endpoint 请参考 https://api.aliyun.com/product/imageaudit
        config.endpoint = f'imageaudit.cn-shanghai.aliyuncs.com'
        return imageaudit20191230Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        # 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例使用环境变量获取 AccessKey 的方式进行调用，仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Sample.create_client(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'])
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
        tasks_0 = imageaudit_20191230_models.ScanTextRequestTasks(
            content='本校小额贷款，安全、快捷、方便、无抵押，随机随贷，当天放款，上门服务。联系weixin 123456'
        )
        scan_text_request = imageaudit_20191230_models.ScanTextRequest(
            tasks=[
                tasks_0
            ],
            labels=[
                labels_0,
                labels_1,
                labels_2,
                labels_3,
                labels_4,
                labels_5,
                labels_6,
                labels_7
            ]
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.scan_text_with_options(scan_text_request, runtime)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        # 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例使用环境变量获取 AccessKey 的方式进行调用，仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Sample.create_client(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'])
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
        tasks_0 = imageaudit_20191230_models.ScanTextRequestTasks(
            content='本校小额贷款，安全、快捷、方便、无抵押，随机随贷，当天放款，上门服务。联系weixin 123456'
        )
        scan_text_request = imageaudit_20191230_models.ScanTextRequest(
            tasks=[
                tasks_0
            ],
            labels=[
                labels_0,
                labels_1,
                labels_2,
                labels_3,
                labels_4,
                labels_5,
                labels_6,
                labels_7
            ]
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.scan_text_with_options_async(scan_text_request, runtime)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error.message)


if __name__ == '__main__':
    Sample.main(sys.argv[1:])
