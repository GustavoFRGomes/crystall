def validate_args(args):
    # if not args.channel:
    #     raise Exception('Channel name is required')
    if (args.resolver and not args.user_info) or (args.user_info and not args.resolver):
        raise Exception('Resolver and user info are required together!')
    if (args.user_email and not args.user_name) or (args.user_name and not args.user_email):
        raise Exception('User email and name are required together!')
    if args.user_email and args.user_name and args.resolver and args.user_info:
        raise Exception('Provided data for both User Email/Name and Resolver/User Info approach given, choose only 1!')
    if not args.user_email and not args.user_name and not args.resolver and not args.user_info:
        raise Exception('No data provided for User Email/Name nor Resolver/User Info approach given, provide 1!')
