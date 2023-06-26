white_pawn_piece = {
    "alias": "w_p",
    "name": "white pawn",
    "pos_x": 0,
    "pos_y": 0,
    "width": 40,
    "height": 40,
    "source": "chess_piece/images",
    "image": ["w_p.png"]
}

black_pawn_piece = {
    "alias": "b_p",
    "name": "black pawn",
    "pos_x": 0,
    "pos_y": 0,
    "width": 40,
    "height": 40,
    "source": "chess_piece/images",
    "image": ["b_p.png"]
}

white_king_piece = {
    "alias": "w_k",
    "name": "white king",
    "pos_x": 0,
    "pos_y": 0,
    "width": 40,
    "height": 40,
    "source": "chess_piece/images",
    "image": ["w_k.png"]
}

black_king_piece = {
    "alias": "b_k",
    "name": "black king",
    "pos_x": 0,
    "pos_y": 0,
    "width": 40,
    "height": 40,
    "source": "chess_piece/images",
    "image": ["b_k.png"]
}

white_queen_piece = {
    "alias": "w_q",
    "name": "white queen",
    "pos_x": 0,
    "pos_y": 0,
    "width": 40,
    "height": 40,
    "source": "chess_piece/images",
    "image": ["w_q.png"]
}

black_queen_piece = {
    "alias": "b_q",
    "name": "black queen",
    "pos_x": 0,
    "pos_y": 0,
    "width": 40,
    "height": 40,
    "source": "chess_piece/images",
    "image": ["b_q.png"]
}

white_knight_piece = {
    "alias": "w_kn",
    "name": "white knight",
    "pos_x": 0,
    "pos_y": 0,
    "width": 40,
    "height": 40,
    "source": "chess_piece/images",
    "image": ["w_kn.png"]
}

black_knight_piece = {
    "alias": "b_kn",
    "name": "black knight",
    "pos_x": 0,
    "pos_y": 0,
    "width": 40,
    "height": 40,
    "source": "chess_piece/images",
    "image": ["b_kn.png"]
}

white_bishop_piece = {
    "alias": "w_b",
    "name": "white bishop",
    "pos_x": 0,
    "pos_y": 0,
    "width": 40,
    "height": 40,
    "source": "chess_piece/images",
    "image": ["w_b.png"]
}

black_bishop_piece = {
    "alias": "b_b",
    "name": "black bishop",
    "pos_x": 0,
    "pos_y": 0,
    "width": 40,
    "height": 40,
    "source": "chess_piece/images",
    "image": ["b_b.png"]
}

white_rock_piece = {
    "alias": "w_r",
    "name": "white rock",
    "pos_x": 0,
    "pos_y": 0,
    "width": 40,
    "height": 40,
    "source": "chess_piece/images",
    "image": ["w_r.png"]
}

black_rock_piece = {
    "alias": "b_r",
    "name": "black rock",
    "pos_x": 0,
    "pos_y": 0,
    "width": 40,
    "height": 40,
    "source": "chess_piece/images",
    "image": ["b_r.png"]
}

_chess_pieces_dict = {}

for val in [item for item in dir() if not item.startswith("__") and item.endswith("piece")]:
    _chess_pieces_dict[eval(val).get("alias")] = eval(val)
    



