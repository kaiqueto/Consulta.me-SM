/*
 * Sprint 4 — "App da farmácia": verificador de receitas assinadas, em Java
 * ========================================================================
 *
 * A farmácia não usa o Consulta.me (nem Python). Ela recebe da clínica 3 arquivos
 * exportados pelo sistema (Sprint 2) e precisa responder: "esta receita é autêntica e íntegra?"
 *
 *   receita-<id>.txt   → os bytes canônicos da receita (exatamente o que foi assinado)
 *   receita-<id>.sig   → a assinatura, em base64 (ECDSA com SHA-256, formato DER)
 *   medico.crt         → certificado X.509 do médico (PEM)
 *   ac.crt             → certificado da AC raiz da clínica (PEM) — a farmácia confia nele
 *
 * Uso (Java 11 ou mais novo roda o arquivo direto, sem compilar à parte):
 *   java farmacia-java/VerificaReceita.java receita-7.txt receita-7.sig medico.crt pki/ac.crt
 *
 * Saída esperada: uma linha "RECEITA VÁLIDA …" ou "RECEITA INVÁLIDA: <motivo>" e código de saída 0 ou 1.
 *
 * Classes-motor da JCA que vocês vão usar: CertificateFactory ("X.509"), X509Certificate,
 * Signature ("SHA256withECDSA") e java.util.Base64.
 *
 * Material de apoio:
 *   - Apostila 06 (Segurança de Redes), seções "Arquitetura de criptografia", "Java: JCA e JCE"
 *     e "Java: assinatura e KeyStore"
 *   - Apostila 04, seção "Cadeia de confiança"
 */
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.util.Base64;

public class VerificaReceita {

    /** Lê um certificado X.509 em PEM (o CertificateFactory aceita PEM diretamente). */
    static X509Certificate carregarCertificado(Path arquivo) throws Exception {
        try (InputStream in = Files.newInputStream(arquivo)) {
            CertificateFactory cf = CertificateFactory.getInstance("X.509");
            return (X509Certificate) cf.generateCertificate(in);
        }
    }

    /**
     * Confere a cadeia: o certificado do médico precisa ter sido assinado pela AC
     * e estar dentro do prazo de validade. Lança exceção (com mensagem clara) se não estiver.
     */
    static void conferirCertificado(X509Certificate medico, X509Certificate ac) throws Exception {
        // TODO Sprint 4: medico.verify(...) com a chave pública da AC e medico.checkValidity()
        throw new UnsupportedOperationException("TODO Sprint 4: conferir o certificado do médico");
    }

    /** Verifica a assinatura ECDSA/SHA-256 dos bytes da receita com a chave pública do médico. */
    static boolean assinaturaValida(byte[] dados, byte[] assinatura, X509Certificate medico) throws Exception {
        // TODO Sprint 4: Signature.getInstance(...), initVerify(...), update(...), verify(...)
        throw new UnsupportedOperationException("TODO Sprint 4: verificar a assinatura");
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 4) {
            System.err.println("Uso: java VerificaReceita.java <receita.txt> <receita.sig> <medico.crt> <ac.crt>");
            System.exit(2);
        }
        byte[] dados = Files.readAllBytes(Path.of(args[0]));
        byte[] assinatura = Base64.getDecoder().decode(Files.readString(Path.of(args[1])).trim());
        X509Certificate medico = carregarCertificado(Path.of(args[2]));
        X509Certificate ac = carregarCertificado(Path.of(args[3]));

        try {
            conferirCertificado(medico, ac);
        } catch (UnsupportedOperationException e) {
            throw e;
        } catch (Exception e) {
            System.out.println("RECEITA INVÁLIDA: certificado do médico não confiável (" + e.getMessage() + ")");
            System.exit(1);
        }

        if (assinaturaValida(dados, assinatura, medico)) {
            System.out.println("RECEITA VÁLIDA — assinada por " + medico.getSubjectX500Principal().getName());
        } else {
            System.out.println("RECEITA INVÁLIDA: a assinatura não confere (o texto foi alterado?)");
            System.exit(1);
        }
    }
}
