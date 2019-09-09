from functions import get_args, report_generator, plot_generator


def main():
    args = get_args()
    report = report_generator(args.state, args.fastfoodtype)
    plot = plot_generator(args.state)
    return report, plot


print(main())

if __name__ == '__main__':
    main()
