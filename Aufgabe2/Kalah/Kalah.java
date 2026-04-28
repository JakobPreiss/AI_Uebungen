package Kalah;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

/**
 * Hauptprogramm für KalahMuster.
 *
 * @since 29.3.2021
 * @author oliverbittel
 */
public class Kalah {

    private static final String ANSI_BLUE = "\u001B[34m";

    /**
     *
     * @param args wird nicht verwendet.
     */
    public static void main(String[] args) {
        //estExample();
        //testHHGame();
        //testMiniMaxAndAlphaBetaWithGivenBoard();
        testHumanMiniMax();
        //testHumanMiniMaxAndAlphaBeta();
    }

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

    //Bewertung Spielsituation
    public static int evaluate(KalahBoard kb) {
        int pitsA = Arrays.stream(kb.getAMulden()).sum();
        int pitsB = Arrays.stream(kb.getBMulden()).sum();
        return (kb.getAKalah() + pitsA) - (kb.getBKalah() + pitsB);
    }

    public static int bestActionWithoutCount(KalahBoard state, int depth) {
        int bestMove = -1;
        int bestScore = Integer.MIN_VALUE;

        for (KalahBoard child : state.possibleActions()) {
            int score = minimax(child, depth - 1, state.getCurPlayer() == 'A'); // false = minimizing (B)
            if (score > bestScore) {
                bestScore = score;
                bestMove = child.getLastPlay();
            }
        }
        return bestMove;
    }

    //minimax
    public static int minimaxWithoutCount(KalahBoard state, int depth, boolean maxPlayer) {
        if (depth == 0 || state.isFinished()) {
            return evaluate(state);
        }

        if (maxPlayer) {
            return state.possibleActions().stream()
                    .mapToInt(child -> minimax(child, depth - 1, false))
                    .max()
                    .orElse(Integer.MIN_VALUE);
        } else {
            return state.possibleActions().stream()
                    .mapToInt(child -> minimax(child, depth - 1, true))
                    .min()
                    .orElse(Integer.MAX_VALUE);
        }
    }

    public static int bestAction(KalahBoard state, int depth) {
        int bestMove = -1;
        int bestScore = Integer.MIN_VALUE;

        for (KalahBoard child : state.possibleActions()) {
            hauefigkeit_minimax += 1;
            int score = minimax(child, depth - 1, state.getCurPlayer() == 'A'); // false = minimizing (B)
            if (score > bestScore) {
                bestScore = score;
                bestMove = child.getLastPlay();
            }
        }
        return bestMove;
    }

    static int hauefigkeit_minimax = 0;
    static int avg_zuege_minimax = 0;
    //minimax
    public static int minimax(KalahBoard state, int depth, boolean maxPlayer) {
        if (depth == 0 || state.isFinished()) {
            return evaluate(state);
        }

        avg_zuege_minimax += 1;

        if (maxPlayer) {
            return state.possibleActions().stream()
                    .mapToInt(child -> minimax(child, depth - 1, false))
                    .max()
                    .orElse(Integer.MIN_VALUE);
        } else {
            return state.possibleActions().stream()
                    .mapToInt(child -> minimax(child, depth - 1, true))
                    .min()
                    .orElse(Integer.MAX_VALUE);
        }
    }

    public static int bestActionWithAlphaBeta(KalahBoard state, int depth) {
        int bestMove = -1;
        int bestScore = Integer.MIN_VALUE;
        int alpha = Integer.MIN_VALUE;
        int beta = Integer.MAX_VALUE;

        for (KalahBoard child : state.possibleActions()) {
            hauefigkeit_minimax_alpha_beta += 1;
            int score = minimaxWithAlphaBeta(child, depth - 1, alpha, beta, child.getCurPlayer() == 'A'); // false = minimizing (B)
            if (score > bestScore) {
                bestScore = score;
                bestMove = child.getLastPlay();
            }
            alpha = Math.max(alpha, bestScore);
        }
        return bestMove;
    }

    static int hauefigkeit_minimax_alpha_beta = 0;
    static int avg_zuege_minimax_alpha_beta = 0;
    //alpha and beta überwachen die beste Aktion und nehmen an, dass der Gegner den besten Zug spielt
    public static int minimaxWithAlphaBeta(KalahBoard state, int depth, int alpha, int beta, boolean maxPlayer) {
        if (depth == 0 || state.isFinished()) {
            return evaluate(state);
        }
        avg_zuege_minimax_alpha_beta += 1;
        if (maxPlayer) {
            int maxEval = Integer.MIN_VALUE;
            for (KalahBoard child : state.possibleActions()) {
                int eval = minimaxWithAlphaBeta(child, depth - 1, alpha, beta, false);
                maxEval = Math.max(maxEval, eval);
                alpha = Math.max(alpha, eval);
                if (alpha >= beta) {
                    break;
                }
            }
            return maxEval;
        } else {
            int minEval = Integer.MAX_VALUE;
            for (KalahBoard child : state.possibleActions()) {
                int eval = minimaxWithAlphaBeta(child, depth - 1, alpha, beta, true);
                minEval = Math.min(minEval, eval);
                beta = Math.min(beta, eval);
                if (beta <= alpha) {
                    break;
                }
            }
            return minEval;
        }
    }

    public static int bestActionWithAlphaBetaAddHeuristic(KalahBoard state, int depth) {
        int bestMove = -1;
        int bestScore = Integer.MIN_VALUE;
        int alpha = Integer.MIN_VALUE;
        int beta = Integer.MAX_VALUE;

        for (KalahBoard child : state.possibleActions()) {
            hauefigkeit_minimax_alpha_beta_heuristic += 1;
            int score = minimaxWithAlphaBetaAddHeuristic(child, depth - 1, alpha, beta, child.getCurPlayer() == 'A'); // false = minimizing (B)
            if (score > bestScore) {
                bestScore = score;
                bestMove = child.getLastPlay();
            }
            alpha = Math.max(alpha, bestScore);
        }
        return bestMove;
    }

    static int hauefigkeit_minimax_alpha_beta_heuristic = 0;
    static int avg_zuege_minimax_alpha_beta_heuristic = 0;
    //alpha and beta überwachen die beste Aktion und nehmen an, dass der Gegner den besten Zug spielt
    public static int minimaxWithAlphaBetaAddHeuristic(KalahBoard state, int depth, int alpha, int beta, boolean maxPlayer) {
        if (depth == 0 || state.isFinished()) {
            return evaluate(state);
        }

        //Erweiterung um eine Heuristik
        List<KalahBoard> possibleActions = state.possibleActions();
        // System.out.println("Heuristik: " + possibleActions.getFirst().getLastPlay());

        avg_zuege_minimax_alpha_beta_heuristic += 1;
        if (maxPlayer) {
            possibleActions.sort(Comparator.comparingInt(child -> -evaluate(child)));

            int maxEval = Integer.MIN_VALUE;
            for (KalahBoard child : possibleActions) {
                int eval = minimaxWithAlphaBetaAddHeuristic(child, depth - 1, alpha, beta, false);
                maxEval = Math.max(maxEval, eval);
                alpha = Math.max(alpha, eval);
                if (alpha >= beta) {
                    break;
                }
            }
            return maxEval;
        } else {
            possibleActions.sort(Comparator.comparingInt(child -> evaluate(child)));

            int minEval = Integer.MAX_VALUE;
            for (KalahBoard child : possibleActions) {
                int eval = minimaxWithAlphaBetaAddHeuristic(child, depth - 1, alpha, beta, true);
                minEval = Math.min(minEval, eval);
                beta = Math.min(beta, eval);
                if (beta <= alpha) {
                    break;
                }
            }
            return minEval;
        }
    }


    public static void testMiniMaxAndAlphaBetaWithGivenBoard() {
        KalahBoard kalahBd = new KalahBoard(new int[]{2, 0, 4, 3, 2, 0, 0, 1, 0, 1, 3, 2, 1, 0}, 'A');
        // A ist am Zug und kann aufgrund von Bonuszügen 8-aml hintereinander ziehen!
        // A muss deutlich gewinnen!

        //Ausgangssituationen

        kalahBd.print();


        while (!kalahBd.isFinished()) {
            int action;
            if (kalahBd.getCurPlayer() == 'A') {
                action = bestActionWithAlphaBeta(kalahBd, 6);
                //action = bestAction(kalahBd, 6);
                System.out.println("A spielt Mulde: " + action + "\n");
            } else {
                action = kalahBd.readAction();
                //action = bestActionWithAlphaBeta(kalahBd, 6);
            }
            kalahBd.move(action);
            kalahBd.print();

        }

        if(kalahBd.getAKalah() > kalahBd.getBKalah()) {
            System.out.println("\n" + ANSI_BLUE + "GAME OVER" + "\n" + ANSI_BLUE + "A hat gewonnen!");
        } else {
            System.out.println("\n" + ANSI_BLUE + "GAME OVER" + "\n" + ANSI_BLUE + "B hat gewonnen!");
        }
    }

    public static void testHumanMiniMax() {
        KalahBoard kalahBd = new KalahBoard();

        // A hat viele Steine auf eigener Seite, B wenig
        //KalahBoard kalahBd = new KalahBoard(new int[]{4, 4, 4, 4, 4, 4, 0, 1, 0, 1, 0, 1, 0, 0}, 'A');

// A bereits im Kalah-Vorteil
        //KalahBoard kalahBd = new KalahBoard(new int[]{3, 3, 3, 3, 3, 3, 6, 1, 1, 1, 1, 1, 1, 0}, 'A');

// A kann sofort Bonuszug erzwingen (Pit 0 hat 6 Steine → landet auf Kalah)
        //KalahBoard kalahBd = new KalahBoard(new int[]{6, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0}, 'A');

// Gegeben aus der Aufgabe (A gewinnt mit 8 Bonuszügen)
        // KalahBoard kalahBd= new KalahBoard(new int[]{2, 0, 4, 3, 2, 0, 0, 1, 0, 1, 3, 2, 1, 0}, 'A');

        kalahBd.print();

        while (!kalahBd.isFinished()) {
            int action;
            if(kalahBd.getCurPlayer() == 'A') {
                action = bestAction(kalahBd, 6);
                bestActionWithAlphaBeta(kalahBd, 6);
                bestActionWithAlphaBetaAddHeuristic(kalahBd, 6);
            } else {
                //action = kalahBd.readAction();
                //action = bestAction(kalahBd, 6);
                //action = bestActionWithAlphaBeta(kalahBd, 6);
                action = bestActionWithoutCount(kalahBd, 6);
            }
            kalahBd.move(action);
            kalahBd.print();
        }

        System.out.println("Minimax:");
        System.out.println("Hauefigkeit: " + hauefigkeit_minimax);
        System.out.println("Aufrufe: " + avg_zuege_minimax);
        System.out.println("Durchschnitt: " + avg_zuege_minimax / hauefigkeit_minimax + "\n");

        System.out.println("Minimax mit Alpha Beta:");
        System.out.println("Hauefigkeit: " + hauefigkeit_minimax_alpha_beta);
        System.out.println("Aufrufe: " + avg_zuege_minimax_alpha_beta);
        System.out.println("Durchschnitt: " + avg_zuege_minimax_alpha_beta / hauefigkeit_minimax_alpha_beta + "\n");

        System.out.println("Minimax mit Alpha Beta + Heuristic:");
        System.out.println("Hauefigkeit: " + hauefigkeit_minimax_alpha_beta_heuristic);
        System.out.println("Aufrufe: " + avg_zuege_minimax_alpha_beta_heuristic);
        System.out.println("Durchschnitt: " + avg_zuege_minimax_alpha_beta_heuristic / hauefigkeit_minimax_alpha_beta_heuristic +"\n");

        if(kalahBd.getAKalah() > kalahBd.getBKalah()) {
            System.out.println("\n" + ANSI_BLUE + "GAME OVER" + "\n" + ANSI_BLUE + "A hat gewonnen!");
        } else {
            System.out.println("\n" + ANSI_BLUE + "GAME OVER" + "\n" + ANSI_BLUE + "B hat gewonnen!");
        }
    }

    public static void testHumanMiniMaxAndAlphaBeta() {
        KalahBoard kalahBd = new KalahBoard();
        kalahBd.print();

        while (!kalahBd.isFinished()) {
            int action;
            if(kalahBd.getCurPlayer() == 'A') {
                //action = bestActionWithAlphaBeta(kalahBd, 6);
                action = bestAction(kalahBd, 6);
            } else {
                action = kalahBd.readAction();
            }
            kalahBd.move(action);
        }

        System.out.println(hauefigkeit_minimax);
        System.out.println(avg_zuege_minimax);

        if(kalahBd.getAKalah() > kalahBd.getBKalah()) {
            System.out.println("\n" + ANSI_BLUE + "GAME OVER" + "\n" + ANSI_BLUE + "A hat gewonnen!");
        } else {
            System.out.println("\n" + ANSI_BLUE + "GAME OVER" + "\n" + ANSI_BLUE + "B hat gewonnen!");
        }
    }
}
