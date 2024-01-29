from QuickPunch.utils import get_supabase, bin_colors, logger

supabase = get_supabase()

class Initialization:
  """
  Initialize the database.
  """
  def __init__(self):
    self.supabase = get_supabase()	

  def clear_database(self):
    """
    Clear the database.
    """
    logger.info(f"{bin_colors.INFO}Clearing database.{bin_colors.ENDC}")
    self.supabase.table("entries").delete().neq("id", 0).execute()
    logger.info(f"{bin_colors.SUCCESS}Database cleared.{bin_colors.ENDC}")
  
  def register_entries(self, entries: list):
    """
    Register the entries in the database.
    """
    logger.info(f"{bin_colors.INFO}Registering entries in database.{bin_colors.ENDC}")
    for i, entry in enumerate(entries):
      self.supabase.table("entries").insert({"id": i, "link": entry}).execute()
    logger.info(f"{bin_colors.SUCCESS}Entries registered in database.{bin_colors.ENDC}")


if __name__ == "__main__":
  initialization = Initialization()
  initialization.clear_database()
  initialization.register_entries(["https://www.youtube.com/watch?v=0b1bLr2vz2s", "https://www.youtube.com/watch?v=0b1bLr2vz2s"])

  