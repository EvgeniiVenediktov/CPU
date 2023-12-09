

class _Snapshot:
    def __init__(self, data:any, instr_id:int, cycle:int) -> None:
        self.data = data
        self.instr_id = instr_id
        self.cycle = cycle

class Snapshooter:
    """Holds and retrieves snapshots indexed by Branch instruction id - `instr_id`"""
    def __init__(self) -> None:
        self.snapshots:list[_Snapshot] = []

    def create_snapshot(self, data:any, instr_id:int, cycle:int) -> None:
        self.snapshots.append(_Snapshot(data, instr_id, cycle))

        # Sorting is probably redundand, but its here for safety
        self.snapshots = sorted(self.snapshots, key=lambda shot: shot.cycle)
    
    def pop_last_matching_snapshot(self, instr_id:int, cycle:int) -> any:
        # Search from the end to get the most recent matching snapshot
        for i in range(len(self.snapshots)-1, -1, -1):
            if self.snapshots[i].instr_id == instr_id and self.snapshots[i].cycle < cycle:
                res = self.snapshots[i].data
                # Delete all more recent snapshots
                self.snapshots = self.snapshots[:i]
                return res
        return None