

class Tile:
    def __init__(self, box, error, b3dm, child_tile_list: list):
        self.box = box
        self.error = error
        self.b3dm = b3dm
        self.child_tile_list = child_tile_list
        self.url = b3dm.lod_dir_name + "/" + b3dm.file_name
        self.name = b3dm.tile_name

    def __iter__(self):
        yield ("boundingVolume", dict(self.box))
        yield ("geometricError", self.error)
        yield ("content", {"url": self.url})
        yield ("extras", {"name": self.name})
        if len(self.child_tile_list) > 0:
            yield ("children", [dict(tile) for tile in self.child_tile_list])

    def dict(self):
        return dict(self)


class RootTile:
    def __init__(self, transform, box, error, child_tile_list):
        self.transform = transform
        self.box = box
        self.error = error
        self.child_tile_list = child_tile_list

    def __iter__(self):
        yield ("transform", self.transform)
        yield ("boundingVolume", dict(self.box))
        yield ("geometricError", self.error)
        yield ("refine", "REPLACE")
        yield ("children", [dict(tile) for tile in self.child_tile_list])

    def dict(self):
        return dict(self)


class Tileset:
    def __init__(self, version, error, root_tile):
        self.version = version
        self.error = error
        self.root_tile = root_tile

    def __iter__(self):
        yield ("asset", {"version": self.version})
        yield ("geometricError", self.error)
        yield ("root", dict(self.root_tile))

    def dict(self):
        return dict(self)

