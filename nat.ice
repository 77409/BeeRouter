






module CONE {


    interface Peer {
        string ping(string peerID);
        string swap();
        string connect(string peerID);
        string pong();
    };

    enum nat_type {
        FULL_CONE,
        RESTRICT_CONE,
        RESTRICT_PORT_CONE,
        SYMMETIC
    } ;
};

