from collections import defaultdict
from datetime import date, timedelta, datetime
from PIL import Image, ImageDraw, ImageFont


class DateUtils(object):
    @staticmethod
    def head_of_calendar(first_date: date) -> date:
        """1日からカレンダーの先頭を計算する。"""
        days_until_sunday = first_date.weekday()
        return first_date - timedelta(days=days_until_sunday)

    @staticmethod
    def end_of_calendar(last_date: date) -> date:
        """最終日からカレンダーの末尾を計算する"""
        days_from_last_saturday = 6 - last_date.weekday()
        return last_date + timedelta(days=days_from_last_saturday)

    @staticmethod
    def generate_default_date_data(start_date: date, end_date: date) -> defaultdict:
        date_data_default = defaultdict(int)
        current_day = start_date
        while current_day <= end_date:
            date_data_default[current_day] = 0
            current_day += timedelta(days=1)
        return date_data_default

    @staticmethod
    def get_month_date_range(target):
        start_date = target.replace(day=1)
        end_date = target.replace(month=target.month % 12 + 1, day=1) - timedelta(days=1)
        return start_date, end_date

    @staticmethod
    def get_month_range_of_today():
        first_day_of_month = datetime.now().replace(day=1)
        last_day_of_month = first_day_of_month.replace(
            month=first_day_of_month.month % 12 + 1, day=1
        ) - timedelta(days=1)
        return first_day_of_month, last_day_of_month


def create_ogp_image(title, book_covers):
    # 新しい画像を生成
    width, height = 1200, 630  # OGP 推奨サイズ
    img = Image.new('RGB', (width, height), color='white')

    d = ImageDraw.Draw(img)
    # タイトルを描画 (実際には、適切なフォントや位置を選択する必要があります)
    font = ImageFont.truetype("arial.ttf", 50)
    d.text((30, 30), title, fill="black", font=font)

    # 書籍のカバーを描画
    for idx, book_cover in enumerate(book_covers):
        book_image = Image.open(book_cover)
        img.paste(book_image, (idx * (book_image.width + 20), height - book_image.height - 20))

    img.save('ogp_image.jpg')
