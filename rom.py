import settings
from worlds.Files import APProcedurePatch, APTokenMixin

class MTPOSettings(settings.group):
    class RomFile(settings.UserFilePath):
        """"Find MTPO ROM."""
        description = "MTPO ROM"
        copy_to = "MTPO.nes"

    rom_file: RomFile = RomFile(RomFile.copy_to)

class MTPOProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Mike Tyson's Punch-Out!!"
    hash = None
    patch_file_ending = ".apmtpo"
    result_file_ending = ".nes"

    procedure = [
        ("apply_tokens", ["token_data"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def patch(self, target: str) -> None:
        with open(target, "wb") as f:
            f.write(self.get_source_data())

def get_base_rom_bytes() -> bytes:
    from . import MTPOWorld
    filename = MTPOWorld.settings.rom_file
    with open(filename, "wb") as f:
        return bytes(f.read())