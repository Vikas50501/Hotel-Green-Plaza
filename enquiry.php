<?php
/**
 * Hotel Green Plaza — enquiry form handler with Hostinger SMTP.
 *
 * ┌──────────────────────────────────────────────────────────────┐
 * │  ONE-TIME SETUP: fill in SMTP_PASS below before going live.  │
 * └──────────────────────────────────────────────────────────────┘
 *
 * Hostinger SMTP settings used here:
 *   Host : mail.hotelgreenplaza.in   (your domain mail server)
 *   Port : 465  (SSL)
 *   Auth : LOGIN
 *   User : info@hotelgreenplaza.in
 *   Pass : <your Hostinger email password>
 */

declare(strict_types=1);

// ─── CONFIGURATION ────────────────────────────────────────────────────────────
const SMTP_HOST    = 'mail.hotelgreenplaza.in';
const SMTP_PORT    = 465;
const SMTP_SECURE  = 'ssl';                      // 'ssl' = port 465 | 'tls' = port 587
const SMTP_USER    = 'info@hotelgreenplaza.in';
const SMTP_PASS    = 'YOUR_EMAIL_PASSWORD_HERE'; // <-- FILL THIS IN
const SMTP_FROM    = 'info@hotelgreenplaza.in';
const SMTP_NAME    = 'Hotel Green Plaza';
const RECIPIENT    = 'info@hotelgreenplaza.in';
const SITE_NAME    = 'Hotel Green Plaza';
const SUCCESS_MSG  = 'Thank you for contacting Hotel Green Plaza. Our team will get back to you shortly.';
// ──────────────────────────────────────────────────────────────────────────────

$wantsJson = isset($_SERVER['HTTP_X_REQUESTED_WITH'])
    && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'fetch';

/* ─────────────────────────────────────────────────── helpers ── */

function respond(bool $ok, string $message, int $status = 200): void
{
    global $wantsJson;
    http_response_code($status);

    if ($wantsJson) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'message' => $message]);
        exit;
    }

    $safe  = htmlspecialchars($message, ENT_QUOTES, 'UTF-8');
    $title = $ok ? 'Enquiry sent' : 'Enquiry not sent';
    header('Content-Type: text/html; charset=utf-8');
    echo <<<HTML
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{$title} | Hotel Green Plaza</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Playfair+Display:wght@600&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
<main id="main">
  <section class="gp-section gp-bg-white" style="padding-top:120px">
    <div class="container">
      <div class="gp-text-center gp-narrow gp-mx-auto">
        <span class="gp-eyebrow">Enquiry</span>
        <h1>{$title}</h1>
        <p class="gp-lead gp-mx-auto">{$safe}</p>
        <div class="gp-btn-group gp-btn-group--center gp-mt-32">
          <a class="gp-btn gp-btn--primary" href="/">Back to Homepage</a>
          <a class="gp-btn gp-btn--secondary" href="/contact.html">Contact Us</a>
        </div>
      </div>
    </div>
  </section>
</main>
</body>
</html>
HTML;
    exit;
}

function field(string $key): string
{
    return trim((string) ($_POST[$key] ?? ''));
}

function clean(string $v): string
{
    return str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v);
}

/* ─────────────────────────────────────────────────── smtp send ── */

/**
 * Minimal self-contained SMTP mailer.
 * Works on Hostinger shared hosting without any external library.
 */
function smtp_send(string $to, string $subject, string $body, string $replyTo = ''): bool
{
    $host    = (SMTP_SECURE === 'ssl' ? 'ssl://' : '') . SMTP_HOST;
    $timeout = 15;
    $errno   = 0;
    $errstr  = '';

    $conn = @fsockopen($host, SMTP_PORT, $errno, $errstr, $timeout);
    if (!$conn) {
        error_log('[HGP SMTP] Connect failed (' . SMTP_HOST . ':' . SMTP_PORT . '): ' . $errstr);
        return false;
    }

    // Read greeting
    fgets($conn, 515);

    // EHLO
    fputs($conn, 'EHLO ' . (gethostname() ?: 'localhost') . "\r\n");
    // Drain multi-line EHLO response
    do { $line = fgets($conn, 515); } while ($line !== false && isset($line[3]) && $line[3] === '-');

    // STARTTLS upgrade (only when using port 587 / 'tls')
    if (SMTP_SECURE === 'tls') {
        fputs($conn, "STARTTLS\r\n");
        fgets($conn, 515);
        stream_socket_enable_crypto($conn, true, STREAM_CRYPTO_METHOD_TLS_CLIENT);
        fputs($conn, 'EHLO ' . (gethostname() ?: 'localhost') . "\r\n");
        do { $line = fgets($conn, 515); } while ($line !== false && isset($line[3]) && $line[3] === '-');
    }

    // AUTH LOGIN
    fputs($conn, "AUTH LOGIN\r\n");
    fgets($conn, 515);
    fputs($conn, base64_encode(SMTP_USER) . "\r\n");
    fgets($conn, 515);
    fputs($conn, base64_encode(SMTP_PASS) . "\r\n");
    $authResp = fgets($conn, 515);

    if (!$authResp || substr($authResp, 0, 3) !== '235') {
        fclose($conn);
        error_log('[HGP SMTP] Authentication failed: ' . trim((string) $authResp));
        return false;
    }

    // Envelope
    fputs($conn, 'MAIL FROM:<' . SMTP_FROM . ">\r\n");
    fgets($conn, 515);

    fputs($conn, 'RCPT TO:<' . $to . ">\r\n");
    fgets($conn, 515);

    // DATA
    fputs($conn, "DATA\r\n");
    fgets($conn, 515);

    // Encode subject for UTF-8
    $encSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';

    $msg  = 'From: ' . SMTP_NAME . ' <' . SMTP_FROM . ">\r\n";
    $msg .= 'To: <' . $to . ">\r\n";
    $msg .= 'Subject: ' . $encSubject . "\r\n";
    if ($replyTo) {
        $msg .= 'Reply-To: <' . $replyTo . ">\r\n";
    }
    $msg .= "MIME-Version: 1.0\r\n";
    $msg .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $msg .= "Content-Transfer-Encoding: 8bit\r\n";
    $msg .= "\r\n";
    $msg .= $body . "\r\n.";

    fputs($conn, $msg . "\r\n");
    $dataResp = fgets($conn, 515);

    fputs($conn, "QUIT\r\n");
    fclose($conn);

    if (!$dataResp || substr($dataResp, 0, 3) !== '250') {
        error_log('[HGP SMTP] DATA rejected: ' . trim((string) $dataResp));
        return false;
    }

    return true;
}

/* ─────────────────────────────────────────────────── guards ── */

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(false, 'This endpoint only accepts form submissions.', 405);
}

// Honeypot — bots fill this; real guests never do
if (field('website') !== '') {
    respond(true, SUCCESS_MSG);
}

/* ─────────────────────────────────────────────────── fields ── */

$name     = field('name');
$phone    = field('phone');
$email    = field('email');
$type     = field('enquiry_type');
$checkin  = field('checkin');
$checkout = field('checkout');
$guests   = field('guests');
$message  = field('message');

$errors = [];

if ($name === '')    { $errors[] = 'Full name is required.'; }
if ($phone === '')   { $errors[] = 'Phone number is required.'; }
if ($message === '') { $errors[] = 'Message is required.'; }

if ($email === '') {
    $errors[] = 'Email address is required.';
} elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'Enter a valid email address.';
}

$allowedTypes = ['Room Booking', 'Restaurant', 'Banquet / Event', 'General Enquiry'];
if (!in_array($type, $allowedTypes, true)) {
    $errors[] = 'Choose an enquiry type.';
}

if ($checkin !== '' && $checkout !== '' && $checkout < $checkin) {
    $errors[] = 'Check-out date must be after the check-in date.';
}

if ($errors) {
    respond(false, implode(' ', $errors), 422);
}

/* ─────────────────────────────────────────────────── build email ── */

$lines = [
    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
    'NEW ENQUIRY — ' . SITE_NAME,
    '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
    '',
    'Enquiry Type : ' . $type,
    'Name         : ' . $name,
    'Phone        : ' . $phone,
    'Email        : ' . $email,
    'Check-in     : ' . ($checkin  ?: '—'),
    'Check-out    : ' . ($checkout ?: '—'),
    'Guests       : ' . ($guests   ?: '—'),
    '',
    'Message:',
    $message,
    '',
    '─────────────────────────────────────────',
    'Submitted from: ' . ($_SERVER['HTTP_HOST'] ?? 'the website'),
    'Date & Time  : ' . date('d M Y, H:i') . ' IST',
];

$subject = clean(sprintf('[%s] %s — %s', SITE_NAME, $type, $name));

$sent = smtp_send(
    RECIPIENT,
    $subject,
    implode("\n", $lines),
    filter_var($email, FILTER_VALIDATE_EMAIL) ? $email : ''
);

if (!$sent) {
    respond(
        false,
        'We could not send your enquiry right now. Please call us at +91 81073 67300 or email info@hotelgreenplaza.in directly.',
        500
    );
}

respond(true, SUCCESS_MSG);
