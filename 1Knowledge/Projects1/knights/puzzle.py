from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO

    # each of them is either a knight or a knave
    Not( And(AKnight, AKnave) ), Or( AKnight, AKnave),
    # Not( And(BKnight, BKnave) ), Or( BKnight, BKnave),
    # Not( And(CKnight, CKnave) ), Or( CKnight, CKnave),

    # A may be a knight if his sentence is true, and a knave otherwise
    Or(
        # A is a knight and says he is both. What he says is true
        And( AKnight, And( AKnight, AKnave ) ),
        # And( AKnight, AKnave ), # simplified version

        # A is a knave and says he is both. What he says is false
        And( AKnave, Not( And( AKnight, AKnave ) ) )
        # And( AKnave, Not(AKnight), Not(AKnave) ) # simplified version
    )

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO

    # each of them is either a knight or a knave
    Not( And(AKnight, AKnave) ), Or( AKnight, AKnave),
    Not( And(BKnight, BKnave) ), Or( BKnight, BKnave),
    # Not( And(CKnight, CKnave) ), Or( CKnight, CKnave),

    # A may be a knight if his sentence is true, and a knave otherwise
    Or(
        # A is a knight and says he is both. What he says is true
        And( AKnight, And( AKnave, BKnave ) ),
        # And( AKnight, AKnave, BKnave ), # simplified version

        # A is a knave and says he is both. What he says is false
        And( AKnave, Not( And( AKnave, BKnave ) ) )
        # And( AKnave, Not(AKnave), Not(BKnave) ) # simplified version
    )

)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

# A says "We are the same kind."
a_sentence2 = Or(
                And(AKnave, BKnave),
                And(AKnight, BKnight)
                )

# B says "We are of different kinds."
b_sentence2 = Or(
                And(AKnave, BKnight),
                And(AKnight, BKnave)
                )

knowledge2 = And(
    # TODO

    # each of them is either a knight or a knave
    Not( And(AKnight, AKnave) ), Or( AKnight, AKnave),
    Not( And(BKnight, BKnave) ), Or( BKnight, BKnave),
    # Not( And(CKnight, CKnave) ), Or( CKnight, CKnave),

    # A may be a knight if his sentence is true, and a knave otherwise
    Or(
        # A is a knight and what he says is true
        And( AKnight, a_sentence2 ),

        # A is a knave and what he says is false
        And( AKnave, Not( a_sentence2 ) )
    )


    ,

    # B may be a knight if his sentence is true, and a knave otherwise
    Or(
        # B is a knight and what he says is true
        And( BKnight, b_sentence2 ),

        # B is a knave and what he says is false
        And( BKnave, Not( b_sentence2 ) )
    )

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."



# A says either "I am a knight." or "I am a knave.", but you don't know which.
a_sentence3 = Or(AKnave, AKnight)


# B says "A said 'I am a knave'."
a_by_b_sentence3 = AKnave
b1_sentence3 = Or(
                    And( AKnight, a_by_b_sentence3),
                    And( AKnave, Not(a_by_b_sentence3) )
                )


# B says "C is a knave."
b2_sentence3 = CKnave

# C says "A is a knight."
c_sentence3 = AKnight


knowledge3 = And(
    # TODO

    # each of them is either a knight or a knave
    Not( And(AKnight, AKnave) ), Or( AKnight, AKnave),
    Not( And(BKnight, BKnave) ), Or( BKnight, BKnave),
    Not( And(CKnight, CKnave) ), Or( CKnight, CKnave),

    # A may be a knight if his sentence is true, and a knave otherwise
    Or(
        # A is a knight and what he says is true
        And( AKnight, a_sentence3 ),

        # A is a knave and what he says is false
        And( AKnave, Not( a_sentence3 ) )
    )

    ,

    # B may be a knight if his sentence is true, and a knave otherwise
    Or(
        # B is a knight and what he says is true
        And( BKnight, b1_sentence3 ),

        # B is a knave and what he says is false
        And( BKnave, Not( b1_sentence3 ) )
    )

    ,

    # B may be a knight if his sentence is true, and a knave otherwise
    Or(
        # B is a knight and what he says is true
        And( BKnight, b2_sentence3 ),

        # B is a knave and what he says is false
        And( BKnave, Not( b2_sentence3 ) )
    )

    ,

    # C may be a knight if his sentence is true, and a knave otherwise
    Or(
        # C is a knight and what he says is true
        And( CKnight, c_sentence3 ),

        # C is a knave and what he says is false
        And( CKnave, Not( c_sentence3 ) )
    )

)




def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
