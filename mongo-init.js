db.createUser(
    {
        user: "garderobe",
        pwd: "garderobe",
        roles: [
            {
                role: "readWrite",
                db: "garderobe"
            }
        ]
    }
);