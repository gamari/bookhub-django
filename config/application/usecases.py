import time
import logging

logger = logging.getLogger("app_logger")
time_logger = logging.getLogger("time_logger")

class Usecase(object):
    def execute(self, *args, **kwargs):
        start_time = time.time()

        try:
            result = self.run(*args, **kwargs)

            end_time = time.time()
            elapsed_time = end_time - start_time

            time_logger.debug(f"[{self.__class__.__name__}] {elapsed_time:.2f} 秒かかりました。\n\n")
            if elapsed_time > 3:
                time_logger.warning(f"[{self.__class__.__name__}] {elapsed_time:.2f} 秒かかりました")

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
