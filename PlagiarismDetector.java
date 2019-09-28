import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class PlagiarismDetector {

    /**
     * the size of tuple, default is 3
     */
    private int tupleSize;

    /**
     * this set refers to all n-word tuples appeared in file2
     */
    private Set<List<String>> file2Set = new HashSet<>();

    /**
     * dictionary for synonyms, key=the word, value=tuple of synonyms of the word(including the word itself)
     */
    private Map<String, Set<String>> synsDict = new HashMap<>();

    private PlagiarismDetector() {
        this.tupleSize = 3;
    }

    private PlagiarismDetector(int tupleSize) {
        this.tupleSize = tupleSize;
    }

    /**
     * Read all synonyms from the synonym file and store them inside self.syns_dict
     * @param synsFile: The name of the synonym file
     */
    private void processSynonym(String synsFile) {
        try {
            File fsyns = new File(synsFile);
            Scanner scanner = new Scanner(fsyns);
            while (scanner.hasNext()) {
                String[] currentWords = scanner.nextLine().split("\\s");
                for (String word : currentWords) {
                    if (this.synsDict.containsKey(word)) {
                        this.synsDict.get(word).addAll(Arrays.asList(currentWords));
                    } else {
                        this.synsDict.put(word, new HashSet<>(Arrays.asList(currentWords)));
                    }
                }
            }
            System.out.println("this.synsDict = " + this.synsDict);
        } catch (FileNotFoundException f) {
            System.err.println("Synonym file not found");
            f.printStackTrace();
            System.exit(1);
        }
    }

    private String removePunctuations(String s) {
        s = s.replace(".", "");
        s = s.replace(",", "");
        // Add more replace calls if necessary
        return s;
    }

    /**
     * Read from input file2, and store all n-size tuples inside a set called self.file2_set
     * By using this set, we can determine whether a tuple appeared in input file2 in O(1) time(average case).
     * @param fileName2: The name of input file2
     */
    private void createTupleSet(String fileName2) {
        try {
            File file2 = new File(fileName2);
            Scanner scanner = new Scanner(file2);
            List<String> readResult = new ArrayList<>();
            while (scanner.hasNext()) {
                readResult.add(scanner.next());
            }

            if (this.tupleSize > readResult.size()) {
                System.err.println("Tuple size should be less than ".concat(String.valueOf(readResult.size())));
                System.exit(1);
            }

            for (int i = 0; i < readResult.size() - tupleSize + 1; i++) {
                this.file2Set.add(readResult.subList(i, i + tupleSize));
            }

        } catch (FileNotFoundException f) {
            System.err.println("File2 not found");
            f.printStackTrace();
            System.exit(1);
        }
    }

    /**
     * This method reads from input file1, and check every tuple in file1 whether it(or it's synonyms)
     * appears in file2. Returns the final result by counting the number of duplicate/plagiarism.
     * @param fileName1 The name of input file1
     * @return The final result, the percent of tuples in file1 which appear in file2
     */
    private String produceOutput(String fileName1) {
        try {
            File file1 = new File(fileName1);
            Scanner scanner = new Scanner(file1);

            List<String> readResult = new ArrayList<>();
            while (scanner.hasNext()) {
                readResult.add(scanner.next());
            }

            if (this.tupleSize > readResult.size()) {
                System.err.println("Tuple size should be less than ".concat(String.valueOf(readResult.size())));
                System.exit(1);
            }

        } catch (FileNotFoundException f) {
            System.err.println("File1 not found");
            f.printStackTrace();
            System.exit(1);
        }

        // TODO Finish this implementation
        return null;
    }


    public static void main(String[] args) {
        System.out.println(Arrays.toString(args));
        // check the number of command line arguments
        if (args.length < 3 || args.length > 4) {
            System.err.println("Usage: java plagiarismDetector syns.txt input_file1 input_file2 (tuple_size=3)");
            System.exit(1);
        }
        System.out.println("HelloWorld!");

        PlagiarismDetector pd;
        if (args.length == 4) {
            pd = new PlagiarismDetector(Integer.parseInt(args[3]));
        } else {
            pd = new PlagiarismDetector();
        }

        pd.processSynonym(args[0]);
        pd.createTupleSet(args[2]);
        System.out.println(pd.produceOutput(args[1]));
    }

}
