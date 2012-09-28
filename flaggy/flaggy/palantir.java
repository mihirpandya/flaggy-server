import java.util.Random;
import java.security.*;

public class GenerateRandomNumbers1 {
        public static void main(String[] args) {
                try {
                        Random random = new Random();
                        String randomInteger;

                        for (int i=0; i<1000000; i++) {
                                randomInteger = new Integer(random.nextInt()).toString();
                                System.out.println(randomInteger);
                        }
                } catch (Exception e) {
                        System.err.println(e);
                }
        }
}


import java.util.Random;
import java.security.*;

public class GenerateRandomNumbers2 {
        public static void main(String[] args) {
                try {
                        SecureRandom random = SecureRandom.getInstance("SHA1PRNG");
                        String randomInteger;

                        for (int i=0; i<1000000; i++) {
                                randomInteger = new Integer(random.nextInt()).toString();
                                System.out.println(randomInteger);
                        }
                } catch (NoSuchAlgorithmException e) {
                        System.err.println(e);
                }
        }
}