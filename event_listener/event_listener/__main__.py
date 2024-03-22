from ..event_listener.consumer import EventListener


def main():
    event_listener = EventListener()
    count = 0
    while True:
        try:
            message = event_listener.listen(1.0)
            if not message:
                continue
            count += 1
            print(f"{count}) {message}")
        except Exception as e:
            print(f"[*] exception occurred: {e}")


if __name__ == "__main__":
    main()
