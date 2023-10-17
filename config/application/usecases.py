import time
import logging

logger = logging.getLogger(__name__)

# TODO ログの処理を実装する

class Usecase(object):
    def execute(self, *args, **kwargs):
        start_time = time.time()

        # 実際のビジネスロジックの実行
        try:
            result = self.run(*args, **kwargs)

            end_time = time.time()
            elapsed_time = end_time - start_time

            # TODO 1秒以上の処理をログに残す
            # logger.info(f"{self.__class__.__name__} executed in {elapsed_time:.2f} seconds")
            print(f"[{self.__class__.__name__}] {elapsed_time:.2f} 秒かかりました")

            return result
        except Exception as e:
            logger.error(f"エラー発生: {self.__class__.__name__}")
            logger.exception(e)
            raise e

    def run(self, *args, **kwargs):
        """
        サブクラスでオーバーライドされるべきメソッド。
        実際のユースケースのビジネスロジックをここに実装する。
        """
        raise NotImplementedError("実装してください")
