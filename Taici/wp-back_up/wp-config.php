<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'taicihrade' );

/** MySQL database username */
define( 'DB_USER', 'taicihrade' );

/** MySQL database password */
define( 'DB_PASSWORD', 'TCnArfdm' );

/** MySQL hostname */
define( 'DB_HOST', 'uvdb33.active24.cz' );

/** Database Charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The Database Collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', 'utf8mb4_unicode_ci' );

/**
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */

define('AUTH_KEY',         's8BtuMOLVe=L-{+GDQmN d%@G:+H)u-)R7W/E,Nq_+U=i!+J:MLA,VBToa6fhR0-');
define('SECURE_AUTH_KEY',  'tx&@W&5K4KV:Z@^@jO0dXnmF3y-:]?xm6_.Sd[;SExw*|Gr`xsr!u0cGNGvR%++j');
define('LOGGED_IN_KEY',    '}eq|Hv@>0]& D+S=lh 7Z4*;^cz&%W,`#fg.$K-2wk>9DL.kO7zjS< N^jZ|()|e');
define('NONCE_KEY',        'dErV.`$tBVXnT<y)g|tGbRd2-4#y9LX~aU^CiXIQ$>-ptIR>NO|iZ:^3aWqm.9MW');
define('AUTH_SALT',        'dPtH5#,D<@eqfFH?g42$8Id*CJr!9yRL-D5.c6]{~v#8Rh=Bd?d2|[o5v^E:<7[N');
define('SECURE_AUTH_SALT', 'nq&>_&T[wma0~ 22R5|N`xZ3@gzf,T;!)IMf<m2=Q/SA o<JBb`Qn/G;R)M_d-+a');
define('LOGGED_IN_SALT',   'eT9-VE[RA!UOf.(|inCURvuFa?i/;qaP6,GMU#rx2w7dy9+fKlMiOI(pFdNT`PB,');
define('NONCE_SALT',       '$zsJ|!Sf,7wUD1>~-:H9PiH3(]_VeBy{Phl=/cRDz{ F|ecwyzXJP<.@{uO,#*d ');


/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'sgud8b_';


define('WP_SITEURL','https://' . ($_SERVER['HTTP_X_WP_TEMPORARY'] ? $_SERVER['HTTP_X_WP_TEMPORARY'] : 'www.taici-hradec.cz'));
define('WP_HOME', 'https://' . ($_SERVER['HTTP_X_WP_TEMPORARY'] ? $_SERVER['HTTP_X_WP_TEMPORARY'] : 'www.taici-hradec.cz'));

define('WP_DEBUG', false);

define('DISALLOW_FILE_EDIT', true);
// vypnutí editace souborů přes admin 

define('FORCE_SSL_ADMIN', true);
// in some setups HTTP_X_FORWARDED_PROTO might contain 
// a comma-separated list e.g. http,https
// so check for https existence
if (strpos($_SERVER['HTTP_X_FORWARDED_PROTO'], 'https') !== false)
       $_SERVER['HTTPS']='on';


/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) )
	define( 'ABSPATH', dirname( __FILE__ ) . '/' );

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
