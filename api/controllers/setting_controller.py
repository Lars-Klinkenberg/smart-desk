import json
from controllers.db_controller import DatabaseController


class SettingController(DatabaseController):
    def save_new_profile(
        self, name, heatmap_steps, daily_goal, standing_height, sitting_height
    ):
        SAVE_END_HEIGHT_QUERY = f"INSERT INTO settings (presetName,heatmap_steps,daily_goal,standing_height,sitting_height) VALUES ('{name}', {heatmap_steps}, {daily_goal}, {standing_height}, {sitting_height});"
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(SAVE_END_HEIGHT_QUERY)
            self.conn.commit()
        except Exception as e:
            raise RuntimeError(e)
        finally:
            self.close()

    def get_profile_by_name(self, name):
        query = f"SELECT * FROM settings WHERE presetName = '{name}';"

        try:
            cursor = self.execute_query(query)
            rows = []

            for (
                id,
                presetName,
                heatmap_steps,
                daily_goal,
                standing_height,
                sitting_height,
            ) in cursor:
                rows.append(
                    {
                        "id": str(id),
                        "presetName": str(presetName),
                        "heatmap_steps": str(heatmap_steps),
                        "daily_goal": str(daily_goal),
                        "standing_height": str(standing_height),
                        "sitting_height": str(sitting_height),
                    }
                )

            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()

    def get_list_of_profiles(self):
        query = f"SELECT * FROM settings;"

        try:
            cursor = self.execute_query(query)
            rows = []

            for (
                id,
                presetName,
                heatmap_steps,
                daily_goal,
                standing_height,
                sitting_height,
            ) in cursor:
                rows.append(
                    {
                        "id": str(id),
                        "presetName": str(presetName),
                        "heatmap_steps": str(heatmap_steps),
                        "daily_goal": str(daily_goal),
                        "standing_height": str(standing_height),
                        "sitting_height": str(sitting_height),
                    }
                )

            return json.dumps(rows)
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()

    def update_profile(
        self, name, heatmap_steps, daily_goal, standing_height, sitting_height
    ):
        query = "UPDATE settings SET "
        updates = []

        # Dynamically add to the query based on which parameters are not None
        if name is None:
            return json.dumps({"error": "preset_name not defined"})

        if heatmap_steps is not None:
            updates.append(f"heatmap_steps = {heatmap_steps}")

        if daily_goal is not None:
            updates.append(f"daily_goal = {daily_goal}")

        if standing_height is not None:
            updates.append(f"standing_height = {standing_height}")

        if sitting_height is not None:
            updates.append(f"sitting_height = {sitting_height}")

        # Ensure that there are updates to make
        if updates:
            # Join the updates and complete the query
            query += ", ".join(updates)
            query += f" WHERE presetName = '{name}'"
        else:
            return json.dumps({"error": "no parameter to change found"})

        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            return json.dumps({"success": "changed config of " + name})
        except Exception as e:
            return json.dumps({"error": str(e)})
        finally:
            self.close()


setting_controller = SettingController()
