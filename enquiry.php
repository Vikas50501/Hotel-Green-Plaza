<?php
/**
 * Hotel Green Plaza — enquiry form handler.
 *
 * The form posts here with fetch() and expects JSON back. Without JavaScript
 * the same POST renders a plain confirmation page, so the form still works.
 *
 * [VERIFY: recipient email address] — set $RECIPIENT below before going live.
 * [VERIFY: mail delivery] — most shared hosts allow mail(); if yours does not,
 * swap the send() call for SMTP (PHPMailer) or your host's transactional API.
 */

declare(strict_types=1);

$RECIPIENT = '';                       // e.g. 'enquiries@hotelgreenplaza.in'
$SITE_NAME = 'Hotel Green Plaza';
$SUCCESS   = 'Thank you for contacting Hotel Green Plaza. Our team will get back to you shortly.';

$wantsJson = isset($_SERVER['HTTP_X_REQUESTED_WITH'])
    && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'fetch';

/* ------------------------------------------------------------------ helpers */

function respond(bool $ok, string $message, int $status = 200): void
{
    global $wantsJson, $SITE_NAME;

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
<title>{$title} | {$SITE_NAME}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&amp;family=Playfair+Display:wght@600&amp;display=swap">
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
          <a class="gp-btn gp-btn--secondary" href="/contact/">Contact Us</a>
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

function clean(string $value): string
{
    // Strip anything that could be used to inject extra mail headers
    return str_replace(["\r", "\n", "%0a", "%0d"], ' ', $value);
}

/* ----------------------------------------------------------------- guards */

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(false, 'This endpoint only accepts form submissions.', 405);
}

// Honeypot — a real guest never fills this in. Report success so bots move on.
if (field('website') !== '') {
    respond(true, $SUCCESS);
}

$name    = field('name');
$phone   = field('phone');
$email   = field('email');
$type    = field('enquiry_type');
$checkin = field('checkin');
$checkout = field('checkout');
$guests  = field('guests');
$message = field('message');

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

/* -------------------------------------------------------------------- send */

if ($RECIPIENT === '') {
    error_log('[Hotel Green Plaza] Enquiry received but $RECIPIENT is not configured.');
    respond(false, 'The enquiry mailbox is not configured yet. Please call us and we will help you straight away.', 500);
}

$lines = [
    'Enquiry type: ' . $type,
    'Name: '         . $name,
    'Phone: '        . $phone,
    'Email: '        . $email,
    'Check-in: '     . ($checkin ?: '—'),
    'Check-out: '    . ($checkout ?: '—'),
    'Guests: '       . ($guests ?: '—'),
    '',
    'Message:',
    $message,
    '',
    '--',
    'Sent from ' . ($_SERVER['HTTP_HOST'] ?? 'the website') . ' on ' . date('d M Y, H:i'),
];

$subject = clean(sprintf('[%s] %s enquiry from %s', $SITE_NAME, $type, $name));
$headers = implode("\r\n", [
    'From: ' . $SITE_NAME . ' <no-reply@' . ($_SERVER['HTTP_HOST'] ?? 'localhost') . '>',
    'Reply-To: ' . clean($name) . ' <' . clean($email) . '>',
    'Content-Type: text/plain; charset=utf-8',
    'MIME-Version: 1.0',
]);

$sent = @mail($RECIPIENT, $subject, implode("\n", $lines), $headers);

if (!$sent) {
    error_log('[Hotel Green Plaza] mail() failed for enquiry from ' . $email);
    respond(false, 'We could not send your enquiry just now. Please call us or email us directly and we will help you straight away.', 500);
}

respond(true, $SUCCESS);
