from simulator.app import run

def main():
    """Entry point: create the app and start the loop."""
    run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
        input("Press Enter to exit...")

