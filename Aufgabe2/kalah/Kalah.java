package kalah;

/**
 * Hauptprogramm für KalahMuster.
 *
 * @since 29.3.2021
 * @author oliverbittel
 */
public class Kalah {

    private static final String ANSI_BLUE = "\u001B[34m";

    private static long numberOfCallsToMinValue = 0;
    private static long numberOfCallsToMaxValue = 0;

    /*
    With SearchDepth 12 and the given Scenario
    Just MiniMax:
    NumberOfCallsToMaxValue: 18919105
    NumberOfCallsToMinValue: 17601171
    Both combined: 36520276

    With Alpha Beta:
    NumberOfCallsToMaxValue: 259681
    NumberOfCallsToMinValue: 210937
    Both combined: 470618

    With Moves ordered:
    NumberOfCallsToMaxValue: 25472
    NumberOfCallsToMinValue: 26005
    Both combined: 51477
    */

    /**
     *
     * @param args wird nicht verwendet.
     */
    public static void main(String[] args) {
        //testExample();
        //testHHGame();
        //testMiniMaxAndAlphaBetaWithGivenBoard(12);
        testHumanMiniMax('A', 8);
        testHumanMiniMaxAndAlphaBeta('A', 12, false);
    }

    private record Modus(Character humanPlayer, int searchDepth, boolean withAlphaBeta, boolean withOrdering) {}

    /**
     * Beispiel von https://de.wikipedia.org/wiki/Kalaha
     */
    public static void testExample() {
        KalahBoard kalahBd = new KalahBoard(new int[]{5, 3, 2, 1, 2, 0, 0, 4, 3, 0, 1, 2, 2, 0}, 'B');
        kalahBd.print();

        System.out.println("B spielt Mulde 11");
        kalahBd.move(11);
        kalahBd.print();

        System.out.println("B darf nochmals ziehen und spielt Mulde 7");
        kalahBd.move(7);
        kalahBd.print();
    }

    /**
     * Mensch gegen Mensch
     */
    public static void testHHGame() {
        KalahBoard kalahBd = new KalahBoard();
        kalahBd.print();

        while (!kalahBd.isFinished()) {
            int action = kalahBd.readAction();
            kalahBd.move(action);
            kalahBd.print();
        }

        System.out.println("\n" + ANSI_BLUE + "GAME OVER");
    }

    public static void testMiniMaxAndAlphaBetaWithGivenBoard(int searchDepth) {
        KalahBoard kalahBd = new KalahBoard(new int[]{2, 0, 4, 3, 2, 0, 0, 1, 0, 1, 3, 2, 1, 0}, 'A');
        // A ist am Zug und kann aufgrund von Bonuszügen 8-aml hintereinander ziehen!
        // A muss deutlich gewinnen!
        kalahBd.print();
        
        Modus mode = new Modus('A', searchDepth, true, false);
        play(kalahBd, mode);
    }

    public static void testHumanMiniMax(char humanPlayer, int searchDepth) {
        Modus mode = new Modus(humanPlayer, searchDepth, false, false);
        play(new KalahBoard(), mode);
    }

    public static void testHumanMiniMaxAndAlphaBeta(char humanPlayer, int searchDepth, boolean withOrdering) {
        Modus mode = new Modus(humanPlayer, searchDepth, true, withOrdering);
        play(new KalahBoard(), mode);
    }

    /**
     * Plays Kalah depending on the given mode and board
     * @param kalahBd the starting board
     * @param mode mode containing info about the human player and the specifics of the algorithm 
     */
    private static void play(KalahBoard kalahBd, Modus mode) {
        kalahBd.print();
        while (!kalahBd.isFinished()) {
            int action;
            if (mode.humanPlayer == null || kalahBd.getCurPlayer() != mode.humanPlayer) {  
                // Berechnen Sie für A eine Aktion mit Ihrem Verfahren und geben Sie die Aktion auf der Konsole aus.
                action = MiniMaxMove(kalahBd.getCurPlayer(), kalahBd, mode.searchDepth, mode);
            }
            else {
                action = kalahBd.readAction();
            }
            kalahBd.move(action);
            kalahBd.print();
        }

        System.out.println("\n" + ANSI_BLUE + "GAME OVER");
        System.out.println("NumberOfCallsToMaxValue: " + numberOfCallsToMaxValue);
        System.out.println("NumberOfCallsToMinValue: " + numberOfCallsToMinValue);
        System.out.println("Both combined: " + (numberOfCallsToMaxValue + numberOfCallsToMinValue));
    }

    /**
     * Invokes the MiniMax algorithm to search for the best move for the given player. Player A tries to get max Value; Player B tries min Value;
     * @param player current player
     * @param board current board situation
     * @return best move given the search depth;
     */
    private static int MiniMaxMove(char player, KalahBoard board, int searchDepth, Modus mode)
    {
        int bestMove = -1;
        int bestValue = player == 'A' ? Integer.MIN_VALUE : Integer.MAX_VALUE;
        int alpha = Integer.MIN_VALUE; //Wert, den A wenigstens erreichen wird
        int beta = Integer.MAX_VALUE; //Wert, den B höchstens erreichen wird

        //Check the value for all possible moves
        for (int move : board.possibleMoves(mode.withOrdering)) {
            KalahBoard nextBoard = new KalahBoard(board);
            boolean moveEndsInOwnKhala = nextBoard.MoveEndsInOwnKhala(move);
            nextBoard.move(move);
            int moveValue; 
            if(player == 'A')
            {
                moveValue = moveEndsInOwnKhala
                    ? MaxValue(nextBoard, searchDepth, alpha, beta, mode)
                    : MinValue(nextBoard, searchDepth, alpha, beta, mode);
            }
            else
            {
                //Player B
                moveValue = moveEndsInOwnKhala
                    ? MinValue(nextBoard, searchDepth, alpha, beta, mode)
                    : MaxValue(nextBoard, searchDepth, alpha, beta, mode);
            }

            //updating the alpha or beta value of the current state
            if(player == 'A' && moveValue > bestValue)
            {
                bestValue = moveValue;
                bestMove = move;
                if(mode.withAlphaBeta) {
                    alpha = Math.max(alpha, moveValue);
                }
            }
            else if((player == 'B' && moveValue < bestValue))
            {
                bestValue = moveValue;
                bestMove = move;
                if(mode.withAlphaBeta) {
                    beta = Math.min(beta, moveValue);
                }
            }

        }
        if(bestMove == -1)
        {
            throw new IllegalArgumentException("Keinen Move gefunden");
        }

        System.out.println("Playing move " + bestMove + " for value: " + bestValue);

        return bestMove;
    }

    /**
     * Searches for the hightest possible Value (best move for A) on the board
     * @param board given board
     * @param searchDepth how far it should search
     * @param alpha best value for A so far
     * @param beta best value for B so far
     * @return hightes Value
     */
    private static int MaxValue(KalahBoard board, int searchDepth, int alpha, int beta, Modus mode)
    {
        numberOfCallsToMaxValue++;
        if(board.isFinished() || searchDepth == 0)
        {
            return BoardValue(board);
        }
        int value = Integer.MIN_VALUE;
        for (int move : board.possibleMoves(mode.withOrdering))
        {
            KalahBoard newBoard = new KalahBoard(board);
            boolean moveEndsInOwnKhala = newBoard.MoveEndsInOwnKhala(move);
            newBoard.move(move);

            value = moveEndsInOwnKhala
                ? Math.max(value, MaxValue(newBoard, searchDepth - 1, alpha, beta, mode)) 
                : Math.max(value, MinValue(newBoard, searchDepth - 1, alpha, beta, mode));

            if(mode.withAlphaBeta) {
                //Check if the value is worse than the currently best one of the upper knot
                if(value >= beta)
                {
                    return value;
                }
                //updating the alpha value of the current knot
                alpha = Math.max(value, alpha);
            }
        }
        return value;
    }

    /**
     * Searches for the lowest possible Value (best move for B) on the board
     * @param board given board
     * @param searchDepth how far it should search
     * @param alpha best value for A so far
     * @param beta best value for B so far
     * @return lowest Value
     */
    private static int MinValue(KalahBoard board, int searchDepth, int alpha, int beta, Modus mode)
    {
        numberOfCallsToMinValue++;
        if(board.isFinished() || searchDepth == 0)
        {
            return BoardValue(board);
        }
        int value = Integer.MAX_VALUE;
        for (int move : board.possibleMoves(mode.withOrdering))
        {
            KalahBoard newBoard = new KalahBoard(board);
            boolean moveEndsInOwnKhala = newBoard.MoveEndsInOwnKhala(move);
            newBoard.move(move);

            value = moveEndsInOwnKhala
                ? Math.min(value, MinValue(newBoard, searchDepth - 1, alpha, beta, mode)) 
                : Math.min(value, MaxValue(newBoard, searchDepth - 1, alpha, beta, mode));

            if(mode.withAlphaBeta) {
                //Check if the value is worse than the currently best one of the upper knot
                if(value <= alpha)
                {
                    return value;
                }
                //updating the beta value of the current knot
                beta = Math.min(value, beta);
            }
        }
        return value;
    }

    /**
     * What's good for B is negative. What's good for A is positive
     * @param board current board
     * @return value for the players
     */
    private static int BoardValue(KalahBoard board)
    {
        return board.getAKalah() - board.getBKalah();
    }
}
