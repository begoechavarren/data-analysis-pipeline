from functions import get_args, report_generator


def main():
    args = get_args()
    report = report_generator(args.state, args.fastfoodcompany)
    return report


print(main())

if __name__ == '__main__':
    main()
