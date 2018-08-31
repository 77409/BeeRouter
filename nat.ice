






module CONE {


    interface Peer {
        string ping(string peerID);
        string swap(string info);
        string connect(string peerID);
        string register(string info);
        string check(string info);
        string pong();
    };

    enum nat_type {
        FULL_CONE,
        RESTRICT_CONE,
        RESTRICT_PORT_CONE,
        SYMMETIC
    } ;
};

