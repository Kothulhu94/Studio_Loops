import json
import os

sess_dir = ".agent/state/sessions"
root_path = ".agent/state/studio_loop_state.json"
orig_id = "the_game_needs_a_start_screen_loading_screen_and_20260511_075538120242"

# 1. Archive any stale new_task session
for f in os.listdir(sess_dir):
    if f.startswith("new_task_"):
        fpath = os.path.join(sess_dir, f)
        with open(fpath) as fp:
            s = json.load(fp)
        s["status"] = "archived"
        s["active"] = False
        with open(fpath, "w") as fp:
            json.dump(s, fp, indent=2)
        print(f"Archived stale session: {f}")

# 2. Load the original session
orig_sess_path = os.path.join(sess_dir, orig_id + ".json")
with open(orig_sess_path) as fp:
    orig = json.load(fp)

print(f"Original session status: {orig['status']}  stage: {orig['current_stage']}")

# 3. Restore root pointer
root = {
    "active_session_id": orig_id,
    "active": True,
    "status": orig["status"],
    "feature": orig["feature"],
    "feature_slug": orig["feature_slug"],
    "current_stage": orig["current_stage"],
    "updated_at": orig.get("updated_at", "")
}
with open(root_path, "w") as fp:
    json.dump(root, fp, indent=2)

print(f"Root pointer restored to: {orig_id}")
print(f"Ready to continue at stage: {orig['current_stage']}")
