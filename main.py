import os.path
import sys
import traceback

#test

from gamescript import game

main_dir = os.path.split(os.path.abspath(__file__))[0]

if __name__ == "__main__":
    error_log = open(os.path.join(main_dir + "/error_report.txt"), "w")
    python_ver = sys.version.split(" ")[0].split(".")
    if int(python_ver[0]) < 3 or int(python_ver[1]) < 10:
        print("This game requires Python version 3.10 and above to run.")
    try:  # for printing error log when error exception happen
        game.Game(main_dir, error_log)
    except Exception:  # Save any error output to txt file for any exception
        traceback.print_exc()
        sys.stdout = error_log
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print("".join("!! " + line for line in lines))  # Log it or whatever here
    error_log.close()
