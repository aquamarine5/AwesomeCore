import requests
import xlrd
import xlwt
import xlrd.book as book
import xlrd.sheet as sheet
import xlwt.Worksheet as wsheet
import datetime


class genshin_gacha_export_standard():
    def __init__(self) -> None:
        print("Beacuse xlrd and xlwt packages only accept .xls format so please convert xlsx to xls first.")
        self.load_data(input("sunfkny/genshin-gacha-export's export xls:"))
        self.load_i18n_data()
        self.init_paimon_data()
        self.load_banner(input("一个空的paimon.moe Wish Export xls表: "))
        # -------
        for i in range(4):
            self.write_sheet(i)
        self.paimon_excel.save(r"D:/result.xls")

    def load_i18n_data(self):
        character_weapon_i18n_en_url = "https://webstatic.mihoyo.com/admin/mi18n/hk4e_cn/20190926_5d8c80193de82/20190926_5d8c80193de82-en-us.json"
        self.i18n_en_data: dict = requests.get(
            character_weapon_i18n_en_url).json()
        character_weapon_i18n_cn_url = "https://webstatic.mihoyo.com/admin/mi18n/hk4e_cn/20190926_5d8c80193de82/20190926_5d8c80193de82-zh-cn.json"
        self.i18n_cn_data: dict = requests.get(
            character_weapon_i18n_cn_url).json()

    def load_data(self,path):
        genshin_gacha_export_data = path
        self.export_excel: book.Book = xlrd.open_workbook(
            genshin_gacha_export_data)

    def init_paimon_data(self):
        def add_gacha_headers(sheet: wsheet):
            sheet.write(0, 0, "Type")
            sheet.write(0, 1, "Name")
            sheet.write(0, 2, "Time")
            sheet.write(0, 3, "⭐")
            sheet.write(0, 4, "Pity")
            sheet.write(0, 5, "#Roll")
            sheet.write(0, 6, "Group")
            sheet.write(0, 7, "Banner")

        def add_banner_headers(sheet: wsheet):
            pass  # Please by hand, sorrrrry~

        def add_info_headers(sheet: wsheet):
            sheet.write(0, 0, "Paimon.moe Wish History Export")
            sheet.write(1, 0, "Version")
            sheet.write(1, 1, "3")
            sheet.write(2, 0, "Export Date")
            sheet.write(2, 1, "2022-01-21 11:45:14")
        self.paimon_excel = xlwt.Workbook()
        add_gacha_headers(self.paimon_excel.add_sheet("Character Event", True))
        add_gacha_headers(self.paimon_excel.add_sheet("Weapon Event", True))
        add_gacha_headers(self.paimon_excel.add_sheet("Standard", True))
        add_gacha_headers(self.paimon_excel.add_sheet("Beginners' Wish", True))
        add_banner_headers(self.paimon_excel.add_sheet("Banner List", True))
        add_info_headers(self.paimon_excel.add_sheet("Information", True))

    def load_banner(self,path):
        paimon_demo_path = path
        paimon_demo_excel: book.Book = xlrd.open_workbook(paimon_demo_path)
        paimon_demo_sheet: sheet.Sheet = paimon_demo_excel.sheet_by_index(4)
        self.banner_list = []
        for i in range(3, 28):
            self.banner_list.append(paimon_demo_sheet.cell_value(i, 0))

    def write_sheet(self, id: int):
        decompiled_sheet = {
            # Before : After
            0: 2,  # Standard
            1: 3,  # Beginner
            2: 0,  # Character
            3: 1  # Weapon
        }
        i18n_type = {
            "武器": "Weapon",
            "角色": "Character"
        }
        i18n_newer = {
            "护摩之杖": "Staff of Homa",
            "安柏": "Amber",
            "西风长枪": "Favonius Lance",
            "祭礼剑": "Sacrificial Sword",
            "丽莎": "Lisa",
            "迪奥娜": "Diona",
            "凯亚": "Kaeya",
            "阿贝多": "Albedo",
            "枫原万叶": "Kaedehara Kazuha",
            "烟绯": "Yanfei",
            "神里绫华": "Kamisato Ayaka",
            "辛焱": "Xinyan",
            "早柚": "Sayu",
            "九条裟罗": "Kujou Sara",
            "罗莎莉亚": "Rosaria",
            "胡桃": "Hu Tao",
            "云堇": "Yun Jin",
            "天空之脊": "Skyward Spine",
            "祭礼大剑": "Sacrificial Greatsword",
            "松籁响起之时": "Song of Broken Pines",
        }
        length_list = {
            0: 322,
            1: 21,
            2: 490,
            3: 233
        }
        gacha: sheet.Sheet = self.export_excel.sheet_by_index(id)
        length = length_list[id]
        roll_reset_time = datetime.date(2020, 9, 28)
        roll_reset_delta = datetime.timedelta(21)
        roll_reset_next = roll_reset_time+roll_reset_delta
        roll_count = 1
        roll_times = 0
        pity_count = 1
        previous_time = datetime.datetime(2007, 3, 4, 12, 12, 12)
        group_count = 1
        for i in range(length):
            if i == 0:
                continue
            time: str = gacha.cell_value(i, 0)
            name: str = gacha.cell_value(i, 1)
            type: str = gacha.cell_value(i, 2)
            star: str = gacha.cell_value(i, 3)
            allcount: str = gacha.cell_value(i, 4)
            undcount: str = gacha.cell_value(i, 5)  # 保底内
            dt = datetime.date.fromisoformat(time.split(" ")[0])
            if dt > roll_reset_next:
                if roll_count == 1:
                    while(dt <= roll_reset_next):
                        roll_reset_next += roll_reset_delta
                        roll_reset_time += roll_reset_delta
                        roll_times += 1
                    rollc = 1
                else:
                    rollc = 1
                    roll_count = 1
                    roll_reset_next += roll_reset_delta
                    roll_reset_time += roll_reset_delta
                    roll_times += 1
            else:
                rollc = roll_count+1
                roll_count += 1
            try:
                trsed_name = list(self.i18n_en_data.values())[
                    list(self.i18n_cn_data.values()).index(name)].replace("Raincutter", "Rainslasher").replace("Jade Orb", "Emerald Orb")
            except ValueError:
                trsed_name = i18n_newer[name]
            trsed_type = i18n_type[type]
            if star == 3:
                pity_count += 1
                pityc = 1
            elif star == 4:
                pityc = pity_count-1
                pity_count = 1
            elif star == 5:
                pity_count += 1
                pityc = undcount
            if id == 0:  # Standard banner
                banner = "Wanderlust Invocation"
            elif id == 1:  # Beginner banner
                banner = "Beginners' Wish"
            elif id == 2:
                banner = self.banner_list[roll_count]
            elif id == 3:
                banner = ""  # :(
            dta = datetime.datetime.fromisoformat(time)
            if dta == previous_time:
                groupc = 1
                group_count = 1
                bsheet.write(i-1, 6, 1)
            else:
                groupc = group_count
                group_count += 1
                previous_time = dta
            # Begin to write
            bsheet: wsheet.Worksheet = self.paimon_excel.get_sheet(
                decompiled_sheet[id])
            bsheet.write(i, 0, trsed_type)
            bsheet.write(i, 1, trsed_name)
            bsheet.write(i, 2, time)
            bsheet.write(i, 3, star)
            bsheet.write(i, 4, pityc)
            bsheet.write(i, 5, rollc)
            bsheet.write(i, 6, groupc)
            bsheet.write(i, 7, banner)


if __name__ == "__main__":
    genshin_gacha_export_standard()
