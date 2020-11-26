class Attendance:
    kodemk: str = ''
    namamk: str = ''
    jumlah_kehadiran: int = 0
    total_pertemuan: int = 0

    # assume all parameters are str,
    # then convert to corresponding type
    def __init__(self, kodemk: str, namamk: str,
                 jumlah_kehadiran: str, total_pertemuan: str):
        self.kodemk = kodemk
        self.namamk = namamk
        self.jumlah_kehadiran = int(jumlah_kehadiran)
        self.total_pertemuan = int(total_pertemuan)
