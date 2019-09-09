from functions import get_args, pdf_generator


def main():
    args = get_args()
    pdf_generator(args.state, args.fastfoodtype)
    return "A pdf file has been generated with your report"


print(main())

if __name__ == '__main__':
    main()
