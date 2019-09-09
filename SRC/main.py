from functions import get_args, email_generator


def main():
    args = get_args()
    email_generator(args.state, args.fastfoodtype)
    pass


if __name__ == '__main__':
    main()
