<?php
if ( ! function_exists('add_action') ) {
		header('Status: 403 Forbidden');
		header('HTTP/1.1 403 Forbidden');
		exit();
}
 
if ( ! current_user_can('manage_options') ) { 
		header('Status: 403 Forbidden');
		header('HTTP/1.1 403 Forbidden');
		exit();
}

?>

<div id="bps-container" class="wrap" style="margin:45px 20px 5px 0px;">

<noscript><div id="message" class="updated" style="font-weight:600;font-size:13px;padding:5px;background-color:#dfecf2;border:1px solid #999;-moz-border-radius-topleft:3px;-webkit-border-top-left-radius:3px;-khtml-border-top-left-radius:3px;border-top-left-radius:3px;-moz-border-radius-topright:3px;-webkit-border-top-right-radius:3px;-khtml-border-top-right-radius:3px;border-top-right-radius:3px;-webkit-box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);-moz-box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);"><span style="color:blue">BPS Warning: JavaScript is disabled in your Browser</span><br />BPS plugin pages will not display visually correct and all BPS JavaScript functionality will not work correctly.</div></noscript>

<?php 
$ScrollTop_options = get_option('bulletproof_security_options_scrolltop');

if ( $ScrollTop_options['bps_scrolltop'] != 'Off' ) {
	
	if ( esc_html($_SERVER['REQUEST_METHOD']) == 'POST' || isset( $_GET['settings-updated'] ) && @$_GET['settings-updated'] == true ) {

		bpsPro_Browser_UA_scroll_animation();
	}
}

## Preloads the w3tc_dashboard page in an iFrame, which writes W3TC htaccess code to the Root htaccess file ONLY if W3TC htaccess code does not already exist.
// The iFrame cannot be loaded in this function: bpsPro_Pwizard_Autofix_W3TC() because things do not happen in time for processing data due to a delay in loading the iFrame.
// Unlock the Root htaccess file if it is locked. Force generate W3TC htaccess code in the Root htaccess file by loading the W3TC Dashboard page in an iFrame.
// Unlock the wp-config.php file if it is locked, writes the WPSC wp-config.php code.
function bpsPro_w3tc_dashboard_iframe_preload() {
	
	if ( isset( $_POST['Submit-Setup-Wizard'] ) ) {
		return;
	}

	$w3tc_plugin = 'w3-total-cache/w3-total-cache.php';
	$w3tc_plugin_active = in_array( $w3tc_plugin, apply_filters('active_plugins', get_option('active_plugins')));

	if ( $w3tc_plugin_active == 1 || is_plugin_active_for_network( $w3tc_plugin ) ) {	

		$rootHtaccess = ABSPATH . '.htaccess';
		
		if ( file_exists($rootHtaccess) ) {
		
			$wpconfig = ABSPATH . 'wp-config.php';
			$sapi_type = php_sapi_name();
			$perms_wpconfig = @substr(sprintf('%o', fileperms($wpconfig)), -4);
			$permsRootHtaccess = @substr(sprintf('%o', fileperms($rootHtaccess)), -4);
				
			if ( @substr($sapi_type, 0, 6) != 'apache' || @$perms_wpconfig != '0666' || @$perms_wpconfig != '0777' ) {
				@chmod( $wpconfig, 0644 );
			}
	
			if ( @substr($sapi_type, 0, 6) != 'apache' || @$permsRootHtaccess != '0666' || @$permsRootHtaccess != '0777' ) {
				chmod( $rootHtaccess, 0644 );
			}

			if ( is_multisite() ) {
				echo '<iframe src="'.network_admin_url( 'admin.php?page=w3tc_dashboard' ).'" style="width:0;height:0;border:0;border:none;"></iframe>';
			} else {
				echo '<iframe src="'.admin_url( 'admin.php?page=w3tc_dashboard' ).'" style="width:0;height:0;border:0;border:none;"></iframe>';
			}
		}
	}
}

bpsPro_w3tc_dashboard_iframe_preload();
?>

<?php
if ( function_exists('get_transient') ) {
require_once( ABSPATH . 'wp-admin/includes/plugin-install.php' );

	if ( false === ( $bps_api = get_transient('bulletproof-security_info') ) ) {
		$bps_api = plugins_api( 'plugin_information', array( 'slug' => stripslashes( 'bulletproof-security' ) ) );
		
		if ( ! is_wp_error( $bps_api ) ) {
			$bps_expire = 60 * 30; // Cache downloads data for 30 minutes
			$bps_downloaded = array( 'downloaded' => $bps_api->downloaded );
			maybe_serialize( $bps_downloaded );
			set_transient( 'bulletproof-security_info', $bps_downloaded, $bps_expire );
		}
	}

		$bps_transient = get_transient( 'bulletproof-security_info' );
    	
		echo '<div class="bps-star-container">';
		echo '<div class="bps-star"><img src="'.plugins_url('/bulletproof-security/admin/images/star.png').'" /></div>';
		echo '<div class="bps-downloaded">';
		
		foreach ( $bps_transient as $key => $value ) {
			echo number_format_i18n( $value ) .' '. str_replace( 'downloaded', "Downloads", $key );
		}
		
		echo '<div class="bps-star-link"><a href="https://wordpress.org/support/view/plugin-reviews/bulletproof-security#postform" target="_blank" title="Add a Star Rating for the BPS plugin">'.__('Rate BPS', 'bulletproof-security').'</a><br><a href="https://affiliates.ait-pro.com/po/" target="_blank" title="Upgrade to BulletProof Security Pro">Upgrade to Pro</a></div>';
		echo '</div>';
		echo '</div>';
}
?>

<div id="message" class="updated" style="border:1px solid #999;background-color:#000;">

<?php

$bps_wpcontent_dir = str_replace( ABSPATH, '', WP_CONTENT_DIR );
$bpsSpacePop = '-------------------------------------------------------------';

if ( isset( $_POST['Submit-Setup-Wizard'] ) ) {
require_once( WP_PLUGIN_DIR . '/bulletproof-security/admin/wizard/wizard-functions.php' );
require_once( WP_PLUGIN_DIR . '/bulletproof-security/admin/wizard/pwizard-autofix.php' );
require_once( WP_PLUGIN_DIR . '/bulletproof-security/admin/wizard/pwizard-autofix-setup.php' );
}

// Wizard Prep: Apache Module directive check to get and create the apache modules and htaccess files enabled|disabled DB options/values.
// .53.6: Create|Update htaccess Files Enabled|Disabled DB option values
// mod_access_compat|mod_authz_core forward/backward compatibility: create new htaccess files if needed
// A user can override this check by choosing Enable or Disable htaccess Files Setup Wizard option.
// Enable override: fallback to create mod_access_compat htaccess files. Only in the case where BPS detects fubar. Otherwise normal htaccess file detection/creation is performed.
// Disable override: htaccess files will either be deleted if they exist or not created and all BPS htaccess features will be disabled.
// Important: DO NOT Add: isset( $_POST['Submit-Wizard-HFiles'] ) 
function bpsPro_pre_installation_prep() {

	if ( isset( $_POST['Submit-Setup-Wizard'] ) || isset( $_POST['Submit-Net-LSM'] ) || isset( $_POST['Submit-Wizard-GDMW'] ) ) {
		return;
	}
	
	bpsPro_apache_mod_directive_check();
}

bpsPro_pre_installation_prep();

require_once( WP_PLUGIN_DIR . '/bulletproof-security/admin/wizard/wizard-backup.php' );

bpsPro_Wizard_deny_all();
bpsPro_root_precheck_download();

// Pre-installation Wizard Pre-Checks - Check if php.ini handler code exists in root .htaccess file, but not in Custom Code
// The bpsSetupWizardCreateRootHtaccess() function will ensure that Custom Code DB options already exist if a php.ini handler is found in the root .htaccess file
// This additional insurance check is needed in cases where users re-run the wizard at a later time & for making error/troubleshooting simpler
// .53.6: Wordfence WAF Firewall mess condition added
function bpsSetupWizardPhpiniHandlerCheck() {
$options = get_option('bulletproof_security_options_customcode');	
$file = ABSPATH . '.htaccess';
$file_contents = @file_get_contents($file);
$successTextBegin = '<font color="green"><strong>';
$successTextEnd = '</strong></font><br>';
$failTextBegin = '<font color="#fb0101"><strong>';
$failTextEnd = '</strong></font><br>';	

	if ( file_exists($file) ) {		

		preg_match_all('/AddHandler|SetEnv PHPRC|suPHP_ConfigPath|Action application/', $file_contents, $matches);
		preg_match_all('/AddHandler|SetEnv PHPRC|suPHP_ConfigPath|Action application/', $options['bps_customcode_one'], $DBmatches);
		
		if ( ! $matches[0] ) {
			echo $successTextBegin.__('Pass! PHP/php.ini handler htaccess code check: Not in use, required or needed for your website/Server', 'bulletproof-security').$successTextEnd;
		return;
		}
	
		if ( $matches[0] && $DBmatches[0] ) {
			echo $successTextBegin.__('Pass! PHP/php.ini handler htaccess code was found in your root .htaccess file AND in BPS Pro Custom Code', 'bulletproof-security').$successTextEnd;
		}
		
		if ( $matches[0] && ! $DBmatches[0] ) {
			
			preg_match_all('/(([#\s]{1,}|)(AddHandler|SetEnv PHPRC|suPHP_ConfigPath|Action application).*\s*){1,}/', $file_contents, $h_matches );			
			
			// .53.6: Wordfence WAF Firewall mess
			if ( stripos( $file_contents, "Wordfence WAF" ) ) {

				$text = '<strong><font color="blue">'.__('Wordfence PHP/php.ini handler htaccess code was found in your root .htaccess file, but was NOT found in BPS Custom Code. ', 'bulletproof-security').'<a href="https://forum.ait-pro.com/forums/topic/wordfence-firewall-wp-contentwflogsconfig-php-file-quarantined/#wordfence-php-handler" target="_blank" title="Wordfence PHP Handler Fix">'.__('Click Here', 'bulletproof-security').'</a>'.__(' for the steps to fix this Wordfence problem before running the Setup Wizard.', 'bulletproof-security').'</font></strong><br>';
				echo $text;	

			} else {

				foreach ( $h_matches[0] as $Key => $Value ) {

					$BPS_CC_Options = array( 'bps_customcode_one' => '# PHP/php.ini handler htaccess code' . "\n" . trim( $Value, " \n\r" ) . "\n\n" . $options['bps_customcode_one'] );	

					foreach( $BPS_CC_Options as $key => $value ) {
						update_option('bulletproof_security_options_customcode', $BPS_CC_Options);
					}
				}
				echo $successTextBegin.__('Pass! PHP/php.ini handler root htaccess code added/created in BPS Pro Custom Code', 'bulletproof-security').$successTextEnd;
			}
		}
	}
}

// General all purpose "Settings Saved." message for forms
if ( current_user_can('manage_options') && wp_script_is( 'bps-accordion', $list = 'queue' ) ) {
if ( isset( $_GET['settings-updated'] ) && @$_GET['settings-updated'] == true) {
	$text = '<p style="font-size:1em;font-weight:bold;padding:2px 0px 2px 5px;margin:0px -11px 0px -11px;background-color:#dfecf2;-webkit-box-shadow: 3px 3px 5px 0px rgba(153,153,153,0.7);-moz-box-shadow: 3px 3px 5px 0px rgba(153,153,153,0.7);box-shadow: 3px 3px 5px 0px rgba(153,153,153,0.7);""><font color="green"><strong>'.__('Settings Saved', 'bulletproof-security').'</strong></font></p>';
	echo $text;
	}
}

/**************************************************/
// BEGIN BPS Setup Wizard Pre-Installation Checks
/**************************************************/

function bpsSetupWizardPrechecks() {

$successTextBegin = '<font color="green"><strong>';
$successMessage = __(' DB Table created Successfully!', 'bulletproof-security');
$successTextEnd = '</strong></font><br>';
$failTextBegin = '<font color="#fb0101"><strong>';
$failMessage = __('Error: Unable to create DB Table ', 'bulletproof-security');
$failTextEnd = '</strong></font><br>';
$sapi_type = php_sapi_name();

	echo '<h3>'.__('Setup Wizard Pre-Installation Checks:', 'bulletproof-security').'</h3>
	<div style="font-size:12px;margin:-10px 0px 10px 0px;font-weight:bold;">'.__('If you see any Red font or Blue font messages displayed below, click the Read Me help button above and read the "Notes" help section before clicking the Setup Wizard button.', 'bulletproof-security').'</div>';   
	
	echo '<div id="Wizard-background" style="max-height:250px;width:85%;overflow:auto;margin:0px;padding:10px;background-color:#dfecf2;border:2px solid #999;-moz-border-radius-topleft:3px;-webkit-border-top-left-radius:3px;-khtml-border-top-left-radius:3px;border-top-left-radius:3px;-moz-border-radius-topright:3px;-webkit-border-top-right-radius:3px;-khtml-border-top-right-radius:3px;border-top-right-radius:3px;-webkit-box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);-moz-box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);">';
	
	echo '<span class="setup-wizard-checks-text">';

	echo '<div style="color:black;font-size:1.13em;font-weight:bold;margin-bottom:0px;margin-top:10px;">'.__('Compatibility & Basic Checks', 'bulletproof-security').'</div>';
	echo '<div id="pw-compatibility" style="border-top:3px solid #999999;border-bottom:3px solid #999999;margin-top:0px;"><p>';

	if ( @substr($sapi_type, 0, 6) != 'apache' && get_filesystem_method() == 'direct') {
		echo $successTextBegin.__('Pass! Compatible Server Configuration: Server API: CGI | WP Filesystem API Method: direct.', 'bulletproof-security').$successTextEnd;
	}
	elseif ( @substr($sapi_type, 0, 6) == 'apache' && preg_match('#\\\\#', ABSPATH, $matches) && get_filesystem_method() == 'direct') {
		echo $successTextBegin.__('Pass! Compatible Server Configuration: Server Type Apache: XAMPP, WAMP, MAMP or LAMP | WP Filesystem API Method: direct.', 'bulletproof-security').$successTextEnd;	
	}
	elseif ( @substr($sapi_type, 0, 6) == 'apache' && ! preg_match('#\\\\#', ABSPATH, $matches) && get_filesystem_method() == 'direct') {
		echo $successTextBegin.__('Pass! Compatible Server Configuration: Server API: DSO | WP Filesystem API Method: direct.', 'bulletproof-security').$successTextEnd;		
	}
	elseif ( @substr($sapi_type, 0, 6) == 'apache' && get_filesystem_method() != 'direct') {
		echo $failTextBegin.__('Server API: Apache DSO Server Configuration | WP Filesystem API Method: ', 'bulletproof-security').get_filesystem_method().$failTextEnd.'<br>'.__('Your Server type is DSO and the WP Filesystem API Method is NOT "direct". You can use the Setup Wizard, but you must first make some one-time manual changes to your website before running the Setup Wizard. Please click this Forum Link for instructions: ', 'bulletproof-security').'<a href="https://forum.ait-pro.com/forums/topic/dso-setup-steps/" target="_blank" title="Link opens in a new Browser window"><strong>'.__('DSO Setup Steps', 'bulletproof-security').'</a></strong><br><br>';			
	}
	
	$memoryLimitM = get_cfg_var('memory_limit');
	$memoryLimit = str_replace('M', '', $memoryLimitM);

	if ( $memoryLimit == '' || ! $memoryLimitM ) {
		//echo '<strong><font color="blue">'.__('Unable to get the PHP Configuration Memory Limit value from the Server. It is recommended that your PHP Configuration Memory Limit is set to at least 128M. Contact your Web Host and ask them what your PHP Configuration Memory Limit is for your website.', 'bulletproof-security').'</font></strong><br>';

	} else {

switch ( $memoryLimit ) {
    case $memoryLimit >= '128':
		echo $successTextBegin.__('Pass! PHP Configuration Memory Limit is set to: ', 'bulletproof-security').$memoryLimit.'M'.$successTextEnd;		
		break;
    case $memoryLimit >= '64' && $memoryLimit < '128':
		echo $successTextBegin.__('Pass! PHP Configuration Memory Limit is set to: ', 'bulletproof-security').$memoryLimit.'M. '.__('It is recommended that you increase your memory limit to at least 128M. Contact your Web Host and ask them to increase your memory limit to the maximum memory limit setting allowed by your Host.', 'bulletproof-security').$successTextEnd;
		break;
    case $memoryLimit > '0' && $memoryLimit < '64':
		echo '<br>'.$failTextBegin.__('Error: Your PHP Configuration Memory Limit is set to: ', 'bulletproof-security').$memoryLimit.'M. '.__('WordPress needs a bare minimum Memory Limit setting of 64M to perform well. Contact your Web Host and ask them to increase your memory limit to the maximum memory limit setting allowed by your Host.', 'bulletproof-security').$failTextEnd.'<br>';	
		break;
 	}
	}

	// .53.6: Apache Module Directive Check & htaccess Files Enabled|Disabled Check
	$HFiles_options = get_option('bulletproof_security_options_htaccess_files');
	$Apache_Mod_options = get_option('bulletproof_security_options_apache_modules');
	
	if ( $Apache_Mod_options['bps_apache_mod_ifmodule'] == 'Yes' ) {
				
		echo $successTextBegin.__('mod_authz_core is Loaded|Order, Allow, Deny directives are supported|BC: Yes|IfModule: Yes', 'bulletproof-security').$successTextEnd;
			
	} elseif ( $Apache_Mod_options['bps_apache_mod_ifmodule'] == 'No' ) {
				
		$HFiles_options = get_option('bulletproof_security_options_htaccess_files');
				
		if ( $HFiles_options['bps_htaccess_files'] == 'enabled' ) {
			echo $successTextBegin.__('Enable|Disable htaccess Files Option set to Enabled: mod_access_compat htaccess files will be created.', 'bulletproof-security').$successTextEnd;
		} else {
			echo $successTextBegin.__('mod_access_compat is Loaded|Order, Allow, Deny directives are supported|IfModule: No', 'bulletproof-security').$successTextEnd;
		}
	
	} elseif ( $Apache_Mod_options['bps_apache_mod_ifmodule'] == 'fubar' || $HFiles_options['bps_htaccess_files'] == 'disabled' ) {
			echo '<strong><font color="blue">'.__('Enable|Disable htaccess Files Option set to Disabled: All BPS htaccess features will be disabled.', 'bulletproof-security').'</font></strong><br>';
	
	} 

	// BPS .52.6: Pre-save UI Theme Skin with Blue Theme if DB option does not exist. function is in general-functions.php
	bpsPro_presave_ui_theme_skin_options();

	// PHP/php.ini htaccess code pre-check - Check if root .htaccess file has php.ini handler code and if that code has been added to BPS Custom Code
	bpsSetupWizardPhpiniHandlerCheck();
	
	// writable checks:
	// folders: /bps-backup/ and /htaccess/ folder
	// files: default.htaccess, secure.htaccess and wpadmin-secure.htaccess
	$htaccess_dir = WP_PLUGIN_DIR . '/bulletproof-security/admin/htaccess';
	$bps_backup_dir = WP_CONTENT_DIR . '/bps-backup';
	$secureHtaccess = $htaccess_dir . '/secure.htaccess';
	$wpadminHtaccess = $htaccess_dir . '/wpadmin-secure.htaccess';
	$defaultHtaccess = $htaccess_dir . '/default.htaccess';	

	if ( is_writable($htaccess_dir) ) {
		echo $successTextBegin.__('Pass! The ', 'bulletproof-security').$htaccess_dir.__(' Folder is writable.', 'bulletproof-security').$successTextEnd;
	} else {
 		echo $failTextBegin.__('Error: The ', 'bulletproof-security').$htaccess_dir.__(' Folder is NOT writable. If your Server type is DSO and the WP Filesystem API Method is NOT "direct" you can use the Setup Wizard, but you must first make some one-time manual changes to your website before running the Setup Wizard. Please click this Forum Link for instructions: ', 'bulletproof-security').'<a href="https://forum.ait-pro.com/forums/topic/dso-setup-steps/" target="_blank" title="Link opens in a new Browser window"><strong>'.__('DSO Setup Steps', 'bulletproof-security').'</a>'.__(' If your Server type is CGI check the folder permissions. Folder permissions should be either 755 or 705.', 'bulletproof-security').$failTextEnd.'<br>';
	}

	if ( is_writable($bps_backup_dir) ) {
		echo $successTextBegin.__('Pass! The ', 'bulletproof-security').$bps_backup_dir.__(' Folder is writable.', 'bulletproof-security').$successTextEnd;
	} else {
 		echo $failTextBegin.__('Error: The ', 'bulletproof-security').$bps_backup_dir.__(' Folder is NOT writable. If your Server type is DSO and the WP Filesystem API Method is NOT "direct" you can use the Setup Wizard, but you must first make some one-time manual changes to your website before running the Setup Wizard. Please click this Forum Link for instructions: ', 'bulletproof-security').'<a href="https://forum.ait-pro.com/forums/topic/dso-setup-steps/" target="_blank" title="Link opens in a new Browser window"><strong>'.__('DSO Setup Steps', 'bulletproof-security').'</a>'.__(' If your Server type is CGI check the folder permissions. Folder permissions should be either 755 or 705.', 'bulletproof-security').$failTextEnd.'<br>';
	}

	if ( is_writable($secureHtaccess) ) {
		echo $successTextBegin.__('Pass! The ', 'bulletproof-security').$secureHtaccess.__(' File is writable.', 'bulletproof-security').$successTextEnd;
	} else {
 		echo $failTextBegin.__('Error: The ', 'bulletproof-security').$secureHtaccess.__(' File is NOT writable. If your Server type is DSO and the WP Filesystem API Method is NOT "direct" you can use the Setup Wizard, but you must first make some one-time manual changes to your website before running the Setup Wizard. Please click this Forum Link for instructions: ', 'bulletproof-security').'<a href="https://forum.ait-pro.com/forums/topic/dso-setup-steps/" target="_blank" title="Link opens in a new Browser window"><strong>'.__('DSO Setup Steps', 'bulletproof-security').'</a>'.__(' If your Server type is CGI check the file permissions. File permissions should be either 644 or 604.', 'bulletproof-security').$failTextEnd.'<br>';
	}
	
	if ( is_writable($wpadminHtaccess) ) {
		echo $successTextBegin.__('Pass! The ', 'bulletproof-security').$wpadminHtaccess.__(' File is writable.', 'bulletproof-security').$successTextEnd;
	} else {
 		echo $failTextBegin.__('Error: The ', 'bulletproof-security').$wpadminHtaccess.__(' File is NOT writable. If your Server type is DSO and the WP Filesystem API Method is NOT "direct" you can use the Setup Wizard, but you must first make some one-time manual changes to your website before running the Setup Wizard. Please click this Forum Link for instructions: ', 'bulletproof-security').'<a href="https://forum.ait-pro.com/forums/topic/dso-setup-steps/" target="_blank" title="Link opens in a new Browser window"><strong>'.__('DSO Setup Steps', 'bulletproof-security').'</a>'.__(' If your Server type is CGI check the file permissions. File permissions should be either 644 or 604.', 'bulletproof-security').$failTextEnd.'<br>';
	}

	if ( is_writable($defaultHtaccess) ) {
		echo $successTextBegin.__('Pass! The ', 'bulletproof-security').$defaultHtaccess.__(' File is writable.', 'bulletproof-security').$successTextEnd;
	} else {
 		echo $failTextBegin.__('Error: The ', 'bulletproof-security').$defaultHtaccess.__(' File is NOT writable. If your Server type is DSO and the WP Filesystem API Method is NOT "direct" you can use the Setup Wizard, but you must first make some one-time manual changes to your website before running the Setup Wizard. Please click this Forum Link for instructions: ', 'bulletproof-security').'<a href="https://forum.ait-pro.com/forums/topic/dso-setup-steps/" target="_blank" title="Link opens in a new Browser window"><strong>'.__('DSO Setup Steps', 'bulletproof-security').'</a>'.__(' If your Server type is CGI check the file permissions. File permissions should be either 644 or 604.', 'bulletproof-security').$failTextEnd.'<br>';
	}

	echo '</p></div><br>'; // end Compatibility & Basic Checks visual section divider
	echo '</span>';
	echo '</div>';
}

/**************************************************/
// END BPS Setup Wizard Pre-Installation Checks
/**************************************************/

/****************************************/
// BEGIN BPS Setup Wizard
/****************************************/

function bpsSetupWizard() {

if ( isset( $_POST['Submit-Setup-Wizard'] ) && current_user_can('manage_options') ) {
	check_admin_referer( 'bps_setup_wizard' );
	set_time_limit(300);

global $wpdb, $wp_version, $bps_version;

$time_start = microtime( true );

$Stable_name = $wpdb->prefix . "bpspro_seclog_ignore";
$Ltable_name = $wpdb->prefix . "bpspro_login_security";
$DBBtable_name = $wpdb->prefix . "bpspro_db_backup";
$MStable_name = $wpdb->prefix . "bpspro_mscan";

$successTextBegin = '<font color="green"><strong>';
$successMessage = __(' DB Table created Successfully!', 'bulletproof-security');
$successTextEnd = '</strong></font><br>';
$failTextBegin = '<font color="#fb0101"><strong>';
$failMessage = __('Error: Unable to create DB Table ', 'bulletproof-security');
$failTextEnd = '</strong></font><br>';
$HFiles_options = get_option('bulletproof_security_options_htaccess_files');

	// 2.9: BPS plugin 30 day review/rating request Dismiss Notice
	$bps_rate_options = 'bulletproof_security_options_rate_free';
	$gmt_offset = get_option( 'gmt_offset' ) * 3600;
	$bps_free_rate_review = mktime(0, 0, 0, date("m")+1, date("d")+1, date("Y"));

	$BPS_Rate_Option = array( 'bps_free_rate_review' => $bps_free_rate_review + $gmt_offset );

	if ( ! get_option( $bps_rate_options ) ) {	
	
		foreach( $BPS_Rate_Option as $key => $value ) {
			update_option('bulletproof_security_options_rate_free', $BPS_Rate_Option);
		}
	}

	$bps_setup_wizard = 'bulletproof_security_options_wizard_free';
	$BPS_Wizard = array( 'bps_wizard_free' => 'wizard' );	
	
	if ( ! get_option( $bps_setup_wizard ) ) {	
		
		foreach( $BPS_Wizard as $key => $value ) {
			update_option('bulletproof_security_options_wizard_free', $BPS_Wizard);
		}
	
	} else {

		foreach( $BPS_Wizard as $key => $value ) {
			update_option('bulletproof_security_options_wizard_free', $BPS_Wizard);
		}
	}

	echo '<h3>'.__('BPS Setup Verification & Error Checks', 'bulletproof-security').'</h3>';
	
	echo '<div style="font-size:12px;margin:-10px 0px 10px 0px;font-weight:bold;">'.__('If you see all Green font messages displayed below, the Setup Wizard setup completed successfully.', 'bulletproof-security').'<br>'.__('If you see any Red font or Blue font messages displayed below, click the Read Me help button above and read the "Notes" help section.', 'bulletproof-security').'<br>'.__('Click the Read Me help button above for a list of recommended BPS Video Tutorials to watch.', 'bulletproof-security').'</div>';
	
	echo '<div id="Wizard-background" style="max-height:250px;width:85%;overflow:auto;margin:0px;padding:10px;background-color:#dfecf2;border:2px solid #999;-moz-border-radius-topleft:3px;-webkit-border-top-left-radius:3px;-khtml-border-top-left-radius:3px;border-top-left-radius:3px;-moz-border-radius-topright:3px;-webkit-border-top-right-radius:3px;-khtml-border-top-right-radius:3px;border-top-right-radius:3px;-webkit-box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);-moz-box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);">';
	
	echo '<span class="setup-wizard-checks-text">';

	// 2.0: Setup Wizard AutoFix (AutoWhitelist|AutoSetup|AutoCleanup): Create & Save Custom Code
	echo '<div style="color:black;font-size:1.13em;font-weight:bold;margin-bottom:0px;margin-top:10px;">'.__('AutoFix (AutoWhitelist|AutoSetup|AutoCleanup)', 'bulletproof-security').'</div>';
	echo '<div id="pw-autofix" style="border-top:3px solid #999999;border-bottom:3px solid #999999;margin-top:0px;"><p>';

	// AutoWhitelist functions
	bpsPro_Pwizard_Autofix_Request_methods();
	bpsPro_Pwizard_Autofix_plugin_skip_bypass_root();
	bpsPro_Pwizard_Autofix_RFI();
	bpsPro_Pwizard_Autofix_BPSQSE_root();
	bpsPro_Pwizard_Autofix_plugin_skip_bypass_wpadmin();
	bpsPro_Pwizard_Autofix_BPSQSE_wpadmin();
	// AutoSetup|AutoCleanup functions
	bpsPro_Pwizard_Autofix_WPSC();
	bpsPro_Pwizard_Autofix_W3TC();
	bpsPro_Pwizard_Autofix_Comet_Cache();
	// 3.2: No longer offering autofix for the EPC plugin.	
	//bpsPro_Pwizard_Autofix_Endurance();
	bpsPro_Pwizard_Autofix_WPFC();
	bpsPro_Pwizard_Autofix_WPR();
	
	echo '</p></div>';

	echo '<div style="color:black;font-size:1.13em;font-weight:bold;margin-bottom:15px;">'.__('BulletProof Security Database Tables Setup', 'bulletproof-security').'</div>';
	echo '<div id="SWDBTables" style="border-top:3px solid #999999;border-bottom:3px solid #999999;margin-top:-10px;"><p>';
	
	if ( $wpdb->get_var( $wpdb->prepare( "SHOW TABLES LIKE %s", $Stable_name ) ) == $Stable_name ) {
		echo $successTextBegin.$Stable_name.$successMessage.$successTextEnd;
	} else {
		echo $failTextBegin.$failMessage.$Stable_name.$failTextEnd;	
	}

	if ( $wpdb->get_var( $wpdb->prepare( "SHOW TABLES LIKE %s", $Ltable_name ) ) == $Ltable_name ) {
		echo $successTextBegin.$Ltable_name.$successMessage.$successTextEnd;
	} else {
		echo $failTextBegin.$failMessage.$Ltable_name.$failTextEnd;	
	}

	if ( $wpdb->get_var( $wpdb->prepare( "SHOW TABLES LIKE %s", $DBBtable_name ) ) == $DBBtable_name ) {
		echo $successTextBegin.$DBBtable_name.$successMessage.$successTextEnd;
	} else {
		echo $failTextBegin.$failMessage.$DBBtable_name.$failTextEnd;	
	}

	if ( $wpdb->get_var( $wpdb->prepare( "SHOW TABLES LIKE %s", $MStable_name ) ) == $MStable_name ) {
		echo $successTextBegin.$MStable_name.$successMessage.$successTextEnd;
	} else {
		echo $failTextBegin.$failMessage.$MStable_name.$failTextEnd;	
	}

	echo '</p></div>';	
	
	echo '<div style="color:black;font-size:1.13em;font-weight:bold;margin-bottom:15px;">'.__('BulletProof Security Core Folders Setup', 'bulletproof-security').'</div>';
	echo '<div id="SWFolders" style="border-top:3px solid #999999;border-bottom:3px solid #999999;margin-top:-10px;"><p>';
	
	$successMessage2 = __(' Folder created Successfully!', 'bulletproof-security');
	$failMessage2 = __('Error: Unable to create Folder ', 'bulletproof-security');

	if ( is_dir( WP_CONTENT_DIR . '/bps-backup' ) ) {	
		echo $successTextBegin.WP_CONTENT_DIR . '/bps-backup'.$successMessage2.$successTextEnd;
	} else {
		echo $failTextBegin.$failMessage2.WP_CONTENT_DIR . '/bps-backup'.$failTextEnd;	
	}	

	if ( is_dir( WP_CONTENT_DIR . '/bps-backup' ) ) {	
		echo $successTextBegin.WP_CONTENT_DIR . '/bps-backup/master-backups'.$successMessage2.$successTextEnd;
	} else {
		echo $failTextBegin.$failMessage2.WP_CONTENT_DIR . '/bps-backup/master-backups'.$failTextEnd;	
	}
	
	if ( is_dir( WP_CONTENT_DIR . '/bps-backup/logs' ) ) {	
		echo $successTextBegin.WP_CONTENT_DIR . '/bps-backup/logs'.$successMessage2.$successTextEnd;
	} else {
		echo $failTextBegin.$failMessage2.WP_CONTENT_DIR . '/bps-backup/logs'.$failTextEnd;	
	}

	if ( is_dir( WP_CONTENT_DIR . '/bps-backup/wp-hashes' ) ) {	
		echo $successTextBegin.WP_CONTENT_DIR . '/bps-backup/wp-hashes'.$successMessage2.$successTextEnd;
	} else {
		echo $failTextBegin.$failMessage2.WP_CONTENT_DIR . '/bps-backup/wp-hashes'.$failTextEnd;	
	}

	echo '</p></div>';
	
	echo '<div style="color:black;font-size:1.13em;font-weight:bold;margin-bottom:15px;">'.__('BulletProof Security Core Files Setup', 'bulletproof-security').'</div>';
	echo '<div id="SWFiles" style="border-top:3px solid #999999;border-bottom:3px solid #999999;margin-top:-10px;"><p>';

	$successMessage3 = __(' File created or updated Successfully!', 'bulletproof-security');
	$failMessage3 = __('Error: Unable to create or update File ', 'bulletproof-security');	
	
	// .53.6: Enable|Disable htaccess Files: set to htaccess Files Disabled - deletes all htaccess files.
	bpsSetupWizard_delete_htaccess_files();

	// .53.6: New htaccess files enabled|disabled condition
	if ( $HFiles_options['bps_htaccess_files'] != 'disabled' ) {	

		$rootHtaccess = ABSPATH . '.htaccess';
		$rootHtaccessBackup = WP_CONTENT_DIR . '/bps-backup/master-backups/root.htaccess';
		$wpadminHtaccess = ABSPATH . 'wp-admin/.htaccess';
		$wpadminHtaccessBackup = WP_CONTENT_DIR . '/bps-backup/master-backups/wpadmin.htaccess';

		bpsSetupWizardCreateRootHtaccess();
		bpsSetupWizardCreateWpadminHtaccess();
		bpsSetupWizardCreateDefaultHtaccess();
	
		$htaccess_dir = WP_PLUGIN_DIR . '/bulletproof-security/admin/htaccess';
		$secureHtaccess = $htaccess_dir . '/secure.htaccess';
		$wpadminHtaccess = $htaccess_dir . '/wpadmin-secure.htaccess';
		$defaultHtaccess = $htaccess_dir . '/default.htaccess';	
		$bps_ARHtaccess = WP_CONTENT_DIR . '/bps-backup/.htaccess';	
		
		if ( is_writable($secureHtaccess) ) {
			echo $successTextBegin.$secureHtaccess.$successMessage3.$successTextEnd;
		} else {
			echo $failTextBegin.$failMessage3.$secureHtaccess.$failTextEnd;	
		}
	
		if ( is_writable($wpadminHtaccess) ) {
			echo $successTextBegin.$wpadminHtaccess.$successMessage3.$successTextEnd;
		} else {
			echo $failTextBegin.$failMessage3.$wpadminHtaccess.$failTextEnd;	
		}
	
		if ( is_writable($defaultHtaccess) ) {
			echo $successTextBegin.$defaultHtaccess.$successMessage3.$successTextEnd;
		} else {
			echo $failTextBegin.$failMessage3.$defaultHtaccess.$failTextEnd;	
		}
	
		if ( file_exists($bps_ARHtaccess) ) {
			echo $successTextBegin.$bps_ARHtaccess.$successMessage3.$successTextEnd;
		} else {
			echo $failTextBegin.$failMessage3.$bps_ARHtaccess.$failTextEnd;	
		}
	} // end if ( $HFiles_options['bps_htaccess_files'] != 'disabled' ) {
	
	$bpsProDBBLogARQ = WP_CONTENT_DIR . '/bps-backup/logs/db_backup_log.txt';
	$bpsProSecLogARQ = WP_CONTENT_DIR . '/bps-backup/logs/http_error_log.txt';
	$mscan_log = WP_CONTENT_DIR . '/bps-backup/logs/mscan_log.txt';

	if ( file_exists($bpsProDBBLogARQ) ) {
		echo $successTextBegin.$bpsProDBBLogARQ.$successMessage3.$successTextEnd;
	} else {
		echo $failTextBegin.$failMessage3.$bpsProDBBLogARQ.$failTextEnd;	
	}

	if ( file_exists($bpsProSecLogARQ) ) {
		echo $successTextBegin.$bpsProSecLogARQ.$successMessage3.$successTextEnd;
	} else {
		echo $failTextBegin.$failMessage3.$bpsProSecLogARQ.$failTextEnd;	
	}

	if ( file_exists($mscan_log) ) {
		echo $successTextBegin.$mscan_log.$successMessage3.$successTextEnd;
	} else {
		echo $failTextBegin.$failMessage3.$mscan_log.$failTextEnd;	
	}

	// .53.6: New htaccess files enabled|disabled condition
	if ( $HFiles_options['bps_htaccess_files'] != 'disabled' ) {

		$bps_denyall_htaccess_renamed = WP_PLUGIN_DIR . '/bulletproof-security/admin/htaccess/.htaccess';
		$security_log_denyall_htaccess = WP_PLUGIN_DIR . '/bulletproof-security/admin/security-log/.htaccess';
		$system_info_denyall_htaccess = WP_PLUGIN_DIR . '/bulletproof-security/admin/system-info/.htaccess';
		$login_denyall_htaccess = WP_PLUGIN_DIR . '/bulletproof-security/admin/login/.htaccess';
		$MMode_denyall_htaccess = WP_PLUGIN_DIR . '/bulletproof-security/admin/maintenance/.htaccess';
		$DBB_denyall_htaccess = WP_PLUGIN_DIR . '/bulletproof-security/admin/db-backup-security/.htaccess';
		$core_denyall_htaccess = WP_PLUGIN_DIR . '/bulletproof-security/admin/core/.htaccess';
		$wizard_denyall_htaccess = WP_PLUGIN_DIR . '/bulletproof-security/admin/wizard/.htaccess';	
		$email_denyall_htaccess = WP_PLUGIN_DIR . '/bulletproof-security/admin/email-log-settings/.htaccess';		
		$mscan_denyall_htaccess = WP_PLUGIN_DIR . '/bulletproof-security/admin/mscan/.htaccess';	
		
		if ( file_exists($bps_denyall_htaccess_renamed) ) {
			echo $successTextBegin.$bps_denyall_htaccess_renamed.$successMessage3.$successTextEnd;
		} else {
			echo $failTextBegin.$failMessage3.$bps_denyall_htaccess_renamed.$failTextEnd;	
		}
	
		if ( file_exists($security_log_denyall_htaccess) ) {
			echo $successTextBegin.$security_log_denyall_htaccess.$successMessage3.$successTextEnd;
		} else {
			echo $failTextBegin.$failMessage3.$security_log_denyall_htaccess.$failTextEnd;	
		}
	
		if ( file_exists($system_info_denyall_htaccess) ) {
			echo $successTextBegin.$system_info_denyall_htaccess.$successMessage3.$successTextEnd;
		} else {
			echo $failTextBegin.$failMessage3.$system_info_denyall_htaccess.$failTextEnd;	
		}
	
		if ( file_exists($login_denyall_htaccess) ) {
			echo $successTextBegin.$login_denyall_htaccess.$successMessage3.$successTextEnd;
		} else {
			echo $failTextBegin.$failMessage3.$login_denyall_htaccess.$failTextEnd;	
		}
	
		if ( file_exists($MMode_denyall_htaccess) ) {
			echo $successTextBegin.$MMode_denyall_htaccess.$successMessage3.$successTextEnd;
		} else {
			echo $failTextBegin.$failMessage3.$MMode_denyall_htaccess.$failTextEnd;	
		}
	
		if ( file_exists($DBB_denyall_htaccess) ) {
			echo $successTextBegin.$DBB_denyall_htaccess.$successMessage3.$successTextEnd;
		} else {
			echo $failTextBegin.$failMessage3.$DBB_denyall_htaccess.$failTextEnd;	
		}
	
		if ( file_exists($core_denyall_htaccess) ) {
			echo $successTextBegin.$core_denyall_htaccess.$successMessage3.$successTextEnd;
		} else {
			echo $failTextBegin.$failMessage3.$core_denyall_htaccess.$failTextEnd;	
		}
	
		if ( file_exists($wizard_denyall_htaccess) ) {
			echo $successTextBegin.$wizard_denyall_htaccess.$successMessage3.$successTextEnd;
		} else {
			echo $failTextBegin.$failMessage3.$wizard_denyall_htaccess.$failTextEnd;	
		}

		if ( file_exists($email_denyall_htaccess) ) {
			echo $successTextBegin.$email_denyall_htaccess.$successMessage3.$successTextEnd;
		} else {
			echo $failTextBegin.$failMessage3.$email_denyall_htaccess.$failTextEnd;	
		}

		if ( file_exists($mscan_denyall_htaccess) ) {
			echo $successTextBegin.$mscan_denyall_htaccess.$successMessage3.$successTextEnd;
		} else {
			echo $failTextBegin.$failMessage3.$mscan_denyall_htaccess.$failTextEnd;	
		}
	} // end if ( $HFiles_options['bps_htaccess_files'] != 'disabled' ) {
	
	echo '</p></div>';

	echo '<div style="color:black;font-size:1.13em;font-weight:bold;margin-bottom:15px;">'.__('BulletProof Security MScan Malware Scanner Setup', 'bulletproof-security').'</div>';
	echo '<div id="MScanWizard" style="border-top:3px solid #999999;border-bottom:3px solid #999999;margin-top:-10px;"><p>';

	bpsPro_presave_mscan_options();
	
	$successMessage4 = __(' DB Option created or updated Successfully!', 'bulletproof-security');

	$bps_option_name_mscan = 'bulletproof_security_options_MScan_log';
	$bps_new_value_mscan = bpsPro_MScan_LogLastMod_wp_secs();
	$BPS_Options_mscan = array( 'bps_mscan_log_date_mod' => $bps_new_value_mscan );

	if ( ! get_option( $bps_option_name_mscan ) ) {	
		update_option('bulletproof_security_options_MScan_log', $BPS_Options_mscan);
		echo $successTextBegin.$bps_option_name_mscan.$successMessage4.$successTextEnd;
	} else {
		update_option('bulletproof_security_options_MScan_log', $BPS_Options_mscan);
		echo $successTextBegin.$bps_option_name_mscan.$successMessage4.$successTextEnd;
	}

	echo '</p></div>';

	echo '<div style="color:black;font-size:1.13em;font-weight:bold;margin-bottom:15px;">'.__('BulletProof Security DB Backup Setup', 'bulletproof-security').'</div>';
	echo '<div id="DBBackup" style="border-top:3px solid #999999;border-bottom:3px solid #999999;margin-top:-10px;"><p>';

	bpsSetupWizard_dbbackup_folder_check();

	$bps_option_name_dbb = 'bulletproof_security_options_DBB_log';
	$bps_new_value_dbb = bpsPro_DBB_LogLastMod_wp_secs();
	$BPS_Options_dbb = array( 'bps_dbb_log_date_mod' => $bps_new_value_dbb );

	if ( ! get_option( $bps_option_name_dbb ) ) {	
		update_option('bulletproof_security_options_DBB_log', $BPS_Options_dbb);
		echo $successTextBegin.$bps_option_name_dbb.$successMessage4.$successTextEnd;
	} else {
		update_option('bulletproof_security_options_DBB_log', $BPS_Options_dbb);
		echo $successTextBegin.$bps_option_name_dbb.$successMessage4.$successTextEnd;
	}	
	
	echo '</p></div>';
	
	echo '<div style="color:black;font-size:1.13em;font-weight:bold;margin-bottom:15px;">'.__('BulletProof Security Hidden Plugin Folders|Files (HPF) Setup', 'bulletproof-security').'</div>';
	echo '<div id="HPFoptions" style="border-top:3px solid #999999;border-bottom:3px solid #999999;margin-top:-10px;"><p>';
	
	$hpf_successMessage = __(' DB Option created or updated Successfully!', 'bulletproof-security');
	$hpf_cron = get_option('bulletproof_security_options_hpf_cron');

	$hpf_cron1 = ! $hpf_cron['bps_hidden_plugins_cron'] ? 'On' : $hpf_cron['bps_hidden_plugins_cron'];
	$hpf_cron2 = ! $hpf_cron['bps_hidden_plugins_cron_frequency'] ? '15' : $hpf_cron['bps_hidden_plugins_cron_frequency'];
	$hpf_cron3 = ! $hpf_cron['bps_hidden_plugins_cron_email'] ? '' : $hpf_cron['bps_hidden_plugins_cron_email'];
	$hpf_cron4 = ! $hpf_cron['bps_hidden_plugins_cron_alert'] ? '' : $hpf_cron['bps_hidden_plugins_cron_alert'];	
		
	$hpf_cron_options = array(
	'bps_hidden_plugins_cron' 			=> $hpf_cron1, 
	'bps_hidden_plugins_cron_frequency' => $hpf_cron2, 
	'bps_hidden_plugins_cron_email' 	=> $hpf_cron3, 
	'bps_hidden_plugins_cron_alert' 	=> $hpf_cron4 
	);

	foreach( $hpf_cron_options as $key => $value ) {
		update_option('bulletproof_security_options_hpf_cron', $hpf_cron_options);
		echo $successTextBegin.$key.$hpf_successMessage.$successTextEnd;
	}	
	
	$hpf_check = get_option('bulletproof_security_options_hidden_plugins');
	$hpf_check1 = ! $hpf_check['bps_hidden_plugins_check'] ? '' : $hpf_check['bps_hidden_plugins_check'];
		
	$hpf_check_options = array( 'bps_hidden_plugins_check' => $hpf_check1 );

	foreach( $hpf_check_options as $key => $value ) {
		update_option('bulletproof_security_options_hidden_plugins', $hpf_check_options);
		echo $successTextBegin.$key.$hpf_successMessage.$successTextEnd;
	}	
	
	echo $successTextBegin.__('Hidden Plugin Folders|Files (HPF) DB Options created or updated Successfully!', 'bulletproof-security').$successTextEnd;
	echo '</p></div>';

	echo '<div style="color:black;font-size:1.13em;font-weight:bold;margin-bottom:15px;">'.__('BulletProof Security Security Log User Agent Filter Setup', 'bulletproof-security').'</div>';
	echo '<div id="SLuserAgentFilter" style="border-top:3px solid #999999;border-bottom:3px solid #999999;margin-top:-10px;"><p>';
	bpsSetupWizard_autoupdate_useragent_filters();
	
	// 2.0|2.3 BugFix: Changed the default option setting to: Do Not Log POST Request Body Data on new BPS installations & upgrades.
	// .52.7: Set Security Log Limit POST Request Body Data option to checked/limited by default
	if ( ! get_option('bulletproof_security_options_sec_log_post_limit') ) {
		
		$SecLog_post_limit_settings = array( 
		'bps_security_log_post_limit' 	=> '', 
		'bps_security_log_post_none' 	=> '1', 
		'bps_security_log_post_max' 	=> '' 
		);
			
		foreach( $SecLog_post_limit_settings as $key => $value ) {
			update_option('bulletproof_security_options_sec_log_post_limit', $SecLog_post_limit_settings);
		}
	}
	
	echo '</p></div>';
	
	echo '<div style="color:black;font-size:1.13em;font-weight:bold;margin-bottom:15px;">'.__('BulletProof Security Email Alerting & Log File Options Setup', 'bulletproof-security').'</div>';
	echo '<div id="SWSmonitor" style="border-top:3px solid #999999;border-bottom:3px solid #999999;margin-top:-10px;"><p>';	
	
	$admin_email = get_option('admin_email');
	$successMessage7 = __(' DB Option created or updated Successfully!', 'bulletproof-security');
	
	$bps_email_options = get_option('bulletproof_security_options_email');
	
	$bps_email_options1 = ! $bps_email_options['bps_send_email_to'] ? $admin_email : $bps_email_options['bps_send_email_to'];
	$bps_email_options2 = ! $bps_email_options['bps_send_email_from'] ? $admin_email : $bps_email_options['bps_send_email_from'];
	$bps_email_options3 = ! $bps_email_options['bps_send_email_cc'] ? '' : $bps_email_options['bps_send_email_cc'];
	$bps_email_options4 = ! $bps_email_options['bps_send_email_bcc'] ? '' : $bps_email_options['bps_send_email_bcc'];
	$bps_email_options5 = ! $bps_email_options['bps_login_security_email'] ? 'lockoutOnly' : $bps_email_options['bps_login_security_email'];
	$bps_email_options6 = ! $bps_email_options['bps_security_log_size'] ? '500KB' : $bps_email_options['bps_security_log_size'];
	$bps_email_options7 = ! $bps_email_options['bps_security_log_emailL'] ? 'email' : $bps_email_options['bps_security_log_emailL'];
	$bps_email_options8 = ! $bps_email_options['bps_dbb_log_email'] ? 'email' : $bps_email_options['bps_dbb_log_email'];
	$bps_email_options9 = ! $bps_email_options['bps_dbb_log_size'] ? '500KB' : $bps_email_options['bps_dbb_log_size'];
	$bps_email_options10 = ! $bps_email_options['bps_mscan_log_size'] ? '500KB' : $bps_email_options['bps_mscan_log_size'];	
	$bps_email_options11 = ! $bps_email_options['bps_mscan_log_email'] ? 'email' : $bps_email_options['bps_mscan_log_email'];	

	$BPS_Options_Email = array(
	'bps_send_email_to' 		=> $bps_email_options1, 
	'bps_send_email_from' 		=> $bps_email_options2, 
	'bps_send_email_cc' 		=> $bps_email_options3, 
	'bps_send_email_bcc' 		=> $bps_email_options4, 
	'bps_login_security_email' 	=> $bps_email_options5, 
	'bps_security_log_size' 	=> $bps_email_options6, 
	'bps_security_log_emailL' 	=> $bps_email_options7, 
	'bps_dbb_log_email' 		=> $bps_email_options8, 
	'bps_dbb_log_size' 			=> $bps_email_options9, 
	'bps_mscan_log_size' 		=> $bps_email_options10, 
	'bps_mscan_log_email' 		=> $bps_email_options11 
	);

	foreach( $BPS_Options_Email as $key => $value ) {
		update_option('bulletproof_security_options_email', $BPS_Options_Email);
		echo $successTextBegin.$key.$successMessage7.$successTextEnd;
	}

	echo '</p></div>';	
	
	echo '<div style="color:black;font-size:1.13em;font-weight:bold;margin-bottom:15px;">'.__('BulletProof Security Login Security & Monitoring Options Setup', 'bulletproof-security').'</div>';
	echo '<div id="SWLoginSecurity" style="border-top:3px solid #999999;border-bottom:3px solid #999999;margin-top:-10px;"><p>';	
	
	$successMessage8 = __(' DB Option created or updated Successfully!', 'bulletproof-security');

	$BPS_LSM_Options = get_option('bulletproof_security_options_login_security');
	// 2.4: Enable Login Security for WooCommerce option is disabled by default in BPS free and cannot be enabled.
	// 2.4: WooCommerce Enable LSM option Dismiss Notice deleted. bulletproof_security_options_setup_wizard_woo db option deleted.
	// 2.3: BugFix: Enable Login Security for WooCommerce option being reset on rerun. Only enable once if the option does not exist.
	// .54.3: New installations of BPS should not display the WooCommerce Enable LSM option Dismiss Notice if WooCommerce is already installed.
	$bps_login_security1 = ! $BPS_LSM_Options['bps_max_logins'] ? '3' : $BPS_LSM_Options['bps_max_logins'];
	$bps_login_security2 = ! $BPS_LSM_Options['bps_lockout_duration'] ? '15' : $BPS_LSM_Options['bps_lockout_duration'];
	$bps_login_security3 = ! $BPS_LSM_Options['bps_manual_lockout_duration'] ? '60' : $BPS_LSM_Options['bps_manual_lockout_duration'];
	$bps_login_security4 = ! $BPS_LSM_Options['bps_max_db_rows_display'] ? '' : $BPS_LSM_Options['bps_max_db_rows_display'];
	$bps_login_security5 = ! $BPS_LSM_Options['bps_login_security_OnOff'] ? 'On' : $BPS_LSM_Options['bps_login_security_OnOff'];
	$bps_login_security6 = ! $BPS_LSM_Options['bps_login_security_logging'] ? 'logLockouts' : $BPS_LSM_Options['bps_login_security_logging'];
	$bps_login_security7 = ! $BPS_LSM_Options['bps_login_security_errors'] ? 'wpErrors' : $BPS_LSM_Options['bps_login_security_errors'];
	$bps_login_security8 = ! $BPS_LSM_Options['bps_login_security_remaining'] ? 'On' : $BPS_LSM_Options['bps_login_security_remaining'];
	$bps_login_security9 = ! $BPS_LSM_Options['bps_login_security_pw_reset'] ? 'enable' : $BPS_LSM_Options['bps_login_security_pw_reset'];
	$bps_login_security10 = ! $BPS_LSM_Options['bps_login_security_sort'] ? 'ascending' : $BPS_LSM_Options['bps_login_security_sort'];

	$BPS_Options_LSM = array(
	'bps_max_logins' 				=> $bps_login_security1, 
	'bps_lockout_duration' 			=> $bps_login_security2, 
	'bps_manual_lockout_duration' 	=> $bps_login_security3, 
	'bps_max_db_rows_display' 		=> $bps_login_security4, 
	'bps_login_security_OnOff' 		=> $bps_login_security5, 
	'bps_login_security_logging' 	=> $bps_login_security6, 
	'bps_login_security_errors' 	=> $bps_login_security7, 
	'bps_login_security_remaining' 	=> $bps_login_security8, 
	'bps_login_security_pw_reset' 	=> $bps_login_security9,  
	'bps_login_security_sort' 		=> $bps_login_security10, 
	'bps_enable_lsm_woocommerce' 	=> ''
	);

	foreach( $BPS_Options_LSM as $key => $value ) {
		update_option('bulletproof_security_options_login_security', $BPS_Options_LSM);
		echo $successTextBegin.$key.$successMessage8.$successTextEnd;	
	}	
	
	// Custom Code - no echo/output: pre-save CC DB options for Custom Code Export|Import features ONLY if DB options do not exist
	bpsSetupWizardCustomCodePresave();
	// BPS MU Tools - no echo/output: pre-save MU Tools DB options for new BPS installations.
	bpsSetupWizardMUToolsPresave();
	
	echo '</p></div>';	
	
	echo '<div style="color:black;font-size:1.13em;font-weight:bold;margin-bottom:15px;">'.__('BulletProof Security JTC-Lite Options Setup', 'bulletproof-security').'</div>';
	echo '<div id="SWJTC-Lite" style="border-top:3px solid #999999;border-bottom:3px solid #999999;margin-top:-10px;"><p>';

	// 2.9: Added new JTC option: bps_jtc_custom_form_error. Defaults to standard JTC CAPTCHA error message.
	$bps_option_name9b = 'bulletproof_security_options_login_security_jtc';
	$successMessage9b = __(' DB Option created or updated Successfully!', 'bulletproof-security');
	$jtc_options = get_option('bulletproof_security_options_login_security_jtc'); 
	
	if ( ! $jtc_options['bps_jtc_custom_roles'] ) {
			$bps_jtc_custom_roles = array( 'bps', '' );
		
	} else {

		foreach ( $jtc_options as $key => $value ) {
		
			if ( $key == 'bps_jtc_custom_roles' ) {
					
				if ( ! is_array($value) ) {
					$bps_jtc_custom_roles = array( 'bps', '' );
				} else { 
					$bps_jtc_custom_roles = $jtc_options['bps_jtc_custom_roles'];
				}
			}
		}
	}
	
	$bps_jtc_custom_form_error = ! $jtc_options['bps_jtc_custom_form_error'] ? '' : $jtc_options['bps_jtc_custom_form_error'];

	$jtc_db_options_new = array(
	'bps_tooltip_captcha_key' 			=> 'jtc', 
	'bps_tooltip_captcha_hover_text' 	=> 'Type/Enter:  jtc', 
	'bps_tooltip_captcha_title' 		=> 'Hover or click the text box below', 
	'bps_tooltip_captcha_logging' 		=> 'Off', 
	'bps_jtc_login_form' 				=> '1', 
	'bps_jtc_register_form' 			=> '', 
	'bps_jtc_lostpassword_form' 		=> '', 
	'bps_jtc_comment_form' 				=> '', 
	'bps_jtc_mu_register_form' 			=> '', 
	'bps_jtc_buddypress_register_form' 	=> '', 
	'bps_jtc_buddypress_sidebar_form' 	=> '', 
	'bps_jtc_administrator' 			=> '', 
	'bps_jtc_editor' 					=> '', 
	'bps_jtc_author' 					=> '', 
	'bps_jtc_contributor' 				=> '', 
	'bps_jtc_subscriber' 				=> '', 
	'bps_jtc_comment_form_error' 		=> '', 
	'bps_jtc_comment_form_label' 		=> '', 
	'bps_jtc_comment_form_input' 		=> '', 
	'bps_jtc_custom_roles' 				=> $bps_jtc_custom_roles, 
	'bps_enable_jtc_woocommerce' 		=> '', 
	'bps_jtc_custom_form_error' 		=> $bps_jtc_custom_form_error 
	);

	if ( ! get_option( $bps_option_name9b ) ) {	
		
		foreach( $jtc_db_options_new as $key => $value ) {
			update_option('bulletproof_security_options_login_security_jtc', $jtc_db_options_new);
			echo $successTextBegin.$key.$successMessage9b.$successTextEnd;	
		}
	
	} else {

		$jtc_db_options = array(
		'bps_tooltip_captcha_key' 			=> $jtc_options['bps_tooltip_captcha_key'], 
		'bps_tooltip_captcha_hover_text' 	=> $jtc_options['bps_tooltip_captcha_hover_text'], 
		'bps_tooltip_captcha_title' 		=> $jtc_options['bps_tooltip_captcha_title'], 
		'bps_tooltip_captcha_logging' 		=> 'Off', 
		'bps_jtc_login_form' 				=> $jtc_options['bps_jtc_login_form'], 
		'bps_jtc_register_form' 			=> '', 
		'bps_jtc_lostpassword_form' 		=> '', 
		'bps_jtc_comment_form' 				=> '', 
		'bps_jtc_mu_register_form' 			=> '', 
		'bps_jtc_buddypress_register_form' 	=> '', 
		'bps_jtc_buddypress_sidebar_form' 	=> '', 
		'bps_jtc_administrator' 			=> '', 
		'bps_jtc_editor' 					=> '', 
		'bps_jtc_author' 					=> '', 
		'bps_jtc_contributor' 				=> '', 
		'bps_jtc_subscriber' 				=> '', 
		'bps_jtc_comment_form_error' 		=> $jtc_options['bps_jtc_comment_form_error'], 
		'bps_jtc_comment_form_label' 		=> $jtc_options['bps_jtc_comment_form_label'], 
		'bps_jtc_comment_form_input' 		=> $jtc_options['bps_jtc_comment_form_input'], 
		'bps_jtc_custom_roles' 				=> $bps_jtc_custom_roles, 
		'bps_enable_jtc_woocommerce' 		=> '', 
		'bps_jtc_custom_form_error' 		=> $bps_jtc_custom_form_error 
		);
	
		foreach( $jtc_db_options as $key => $value ) {
			update_option('bulletproof_security_options_login_security_jtc', $jtc_db_options);
			echo $successTextBegin.$key.$successMessage9b.$successTextEnd;
		}
	}	

	echo '</p></div>';

	echo '</span>';

	echo '<div id="message" class="updated" style="background-color:#dfecf2;border:1px solid #999;-moz-border-radius-topleft:3px;-webkit-border-top-left-radius:3px;-khtml-border-top-left-radius:3px;border-top-left-radius:3px;-moz-border-radius-topright:3px;-webkit-border-top-right-radius:3px;-khtml-border-top-right-radius:3px;border-top-right-radius:3px;-webkit-box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);-moz-box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);"><p>';
	$text = '<strong><font color="green">'.__('The Setup Wizard has completed BPS Setup.', 'bulletproof-security').'<br>'.__('Check the "BPS Setup Verification & Error Checks" section below for any errors in Red Font.', 'bulletproof-security').'</font></strong><br>';
	echo $text;
	echo '</p></div>';

	$time_end = microtime( true );
	$wizard_run_time = $time_end - $time_start;
	$wizard_time_display = '<strong>'.__('Setup Wizard Completion Time: ', 'bulletproof-security').'</strong>'. round( $wizard_run_time, 2 ) . ' Seconds';	
	
	echo '<div id="message" class="updated" style="background-color:#dfecf2;border:1px solid #999;-moz-border-radius-topleft:3px;-webkit-border-top-left-radius:3px;-khtml-border-top-left-radius:3px;border-top-left-radius:3px;-moz-border-radius-topright:3px;-webkit-border-top-right-radius:3px;-khtml-border-top-right-radius:3px;border-top-right-radius:3px;-webkit-box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);-moz-box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);"><p>';
	echo bpsPro_memory_resource_usage();
	echo $wizard_time_display;
	echo '</p></div>';

	echo '</div>';
	} // end if (isset($_POST['Submit-Setup-Wizard'])
}
/****************************************/
// END BPS Setup Wizard
/****************************************/
?>

</div>

<h2 class="bps-tab-title"><?php _e('BulletProof Security ~ Setup Wizard', 'bulletproof-security'); ?></h2>

<!-- jQuery UI Tab Menu -->
<div id="bps-tabs" class="bps-menu">
    <div id="bpsHead"><img src="<?php echo plugins_url('/bulletproof-security/admin/images/bps-free-logo.gif'); ?>" />
    
<style>
<!--
.bps-spinner {
    visibility:visible;
	position:fixed;
    top:7%;
    left:45%;
 	width:240px;
	background:#fff;
	border:4px solid black;
	padding:2px 0px 4px 8px;   
	z-index:99999;
}

.bps-readme-table {background:#fff;vertical-align:text-top;margin:8px 0px 10px 0px;}
.bps-readme-table-td {padding:5px;}
-->
</style> 

    <div id="bps-spinner" class="bps-spinner" style="visibility:hidden;">
    	<img id="bps-img-spinner" src="<?php echo plugins_url('/bulletproof-security/admin/images/bps-spinner.gif'); ?>" style="float:left;margin:0px 20px 0px 0px;" />
        <div id="bps-spinner-text-btn" style="padding:20px 0px 26px 0px;font-size:14px;">Processing...<br><button style="margin:10px 0px 0px 10px;" onclick="javascript:history.go(-1)">Cancel</button>
		</div>
    </div> 
    
<script type="text/javascript">
/* <![CDATA[ */
function bpsSpinnerSWizard() {
	
    var r = confirm("You can re-run the Setup Wizard again at any time. Your existing settings will NOT be overwritten and will be re-saved. Any new or additional settings that the Setup Wizard finds on your website will be saved/setup.\n\n-------------------------------------------------------------\n\nClick OK to Run the Setup Wizard or click Cancel.");
	
	var img = document.getElementById("bps-spinner"); 

	if (r == true) {
 	
		img.style.visibility = "visible";
	
	} else {
	
		history.go(-1);
	}
}
/* ]]> */
</script>  

    </div>
		<ul>
            <li><a href="#bps-tabs-1"><?php _e('Setup Wizard', 'bulletproof-security'); ?></a></li>
            <li><a href="#bps-tabs-2"><?php _e('Setup Wizard Options', 'bulletproof-security'); ?></a></li>
		</ul>
            
<div id="bps-tabs-1" class="bps-tab-page">

<?php
function bpsPro_hfiles_inpage_message() {       

$HFiles_options = get_option('bulletproof_security_options_htaccess_files');
       
	if ( $HFiles_options['bps_htaccess_files'] == 'disabled' ) {	   
	    $text = '<div style="background-color:#dfecf2;border:1px solid #999;font-weight:bold;padding:0px 5px;margin:0px 0px 10px 0px;-moz-border-radius-topleft:3px;-webkit-border-top-left-radius:3px;-khtml-border-top-left-radius:3px;border-top-left-radius:3px;-moz-border-radius-topright:3px;-webkit-border-top-right-radius:3px;-khtml-border-top-right-radius:3px;border-top-right-radius:3px;-webkit-box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);-moz-box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);box-shadow: 3px 3px 5px -1px rgba(153,153,153,0.7);"><font color="blue">'.__('htaccess Files Disabled Notice: ', 'bulletproof-security').'</font><br><font color="black">'.__('BPS has detected that htaccess files cannot be used on your website/server. Click this ', 'bulletproof-security').'</font><a href="https://forum.ait-pro.com/forums/topic/htaccess-files-disabled-setup-wizard-enable-disable-htaccess-files/" target="_blank" title="htaccess Files Disabled Forum Topic">'.__('htaccess Files Disabled Forum Topic', 'bulletproof-security').'</a><font color="black">'.__(' link for more information before running the Wizards.', 'bulletproof-security').'</font></div>';
		echo $text;
	}
}

bpsPro_hfiles_inpage_message();

?>

<table width="100%" border="0" cellspacing="0" cellpadding="0" class="bps-help_faq_table">
  <tr>
    <td class="bps-table_title">
<?php $text = '<h2>'.__('Setup Wizard ~ ', 'bulletproof-security').'<span style="font-size:.75em;">'.__('One-Click Complete Setup', 'bulletproof-security').'</span></h2><div class="promo-text">'.__('Want even more security protection?', 'bulletproof-security').'<br>'.__('Protect all of your website files with AutoRestore|Quarantine Intrusion Detection & Prevention System: ', 'bulletproof-security').'<a href="https://affiliates.ait-pro.com/po/" target="_blank" title="BPS Pro ARQ IDPS">'.__('Get BPS Pro ARQ IDPS', 'bulletproof-security').'</a><br>'.__('Protect against SpamBot & HackerBot (auto-registering, auto-logins, auto-posting, auto-commenting): ', 'bulletproof-security').'<a href="https://affiliates.ait-pro.com/po/" target="_blank" title="BPS Pro JTC Anti-Spam|Anti-Hacker">'.__('Get BPS Pro JTC Anti-Spam|Anti-Hacker', 'bulletproof-security').'</a><br>'.__('Protect all of your Plugins (plugin folders and files) with an IP Firewall: ', 'bulletproof-security').'<a href="https://affiliates.ait-pro.com/po/" target="_blank" title="BPS Pro Plugin Firewall">'.__('Get BPS Pro Plugin Firewall', 'bulletproof-security').'</a><br>'.__('Protect your WordPress uploads folder against remote access or execution of files: ', 'bulletproof-security').'<a href="https://affiliates.ait-pro.com/po/" target="_blank" title="BPS Pro Uploads Anti-Exploit Guard">'.__('Get BPS Pro Uploads Anti-Exploit Guard', 'bulletproof-security').'</a></div>'; echo $text; ?>
    </td>
  </tr>
  <tr>
    <td class="bps-table_cell_help">
    
<h3 style="margin:0px 0px 5px 0px;"><?php _e('Setup Wizard', 'bulletproof-security'); ?>  <button id="bps-open-modal1" class="button bps-modal-button"><?php _e('Read Me', 'bulletproof-security'); ?></button></h3>

<div id="bps-modal-content1" class="bps-dialog-hide" title="<?php _e('Setup Wizard', 'bulletproof-security'); ?>">

 <table width="100%" border="0" cellspacing="0" cellpadding="0" class="bps-readme-table">
  <tr>
    <td class="bps-readme-table-td">
	
	<?php 
	$text = '<strong>'.__('This Read Me Help window is draggable (top) and resizable (bottom right corner)', 'bulletproof-security').'</strong><br><br>'; 
	echo $text; 
	$text = '<strong><font color="blue">'.__('Recommended Video Tutorials: ', 'bulletproof-security').'</font></strong><br>'; 
	echo $text; 
	?>
	
    <strong><a href="https://forum.ait-pro.com/video-tutorials/#custom-code" title="Custom Code Video Tutorial" target="_blank"><?php _e('Custom Code Video Tutorial', 'bulletproof-security'); ?></a></strong><br /> 
	<strong><a href="https://forum.ait-pro.com/video-tutorials/#security-log-firewall" title="Security Log Video Tutorial" target="_blank"><?php _e('Security Log Video Tutorial', 'bulletproof-security'); ?></a></strong><br /><br />
    
	<?php
 	$text = '<strong>'.__('Setup Wizard Steps: ', 'bulletproof-security').'</strong><br>'.__('1. Click the Setup Wizard button.', 'bulletproof-security').'<br><br>';
	
	echo $text;    

	$text = '<strong>'.__('Notes: ', 'bulletproof-security').'</strong><br>'.__('Setup Wizard Pre-Installation Checks are automatically performed and displayed on the Setup Wizard page. Green font messages mean everything is good. Red and blue font messages are displayed with an exact description of the issue and how to correct the issue. Red font error messages need to be fixed before running the Setup Wizard. Blue font messages can either be a recommendation or a notice about something. Blue font messages do not need to be fixed before running the Setup Wizard.', 'bulletproof-security').'<br><br>'.__('You can re-run the Setup Wizard again at any time. Your existing settings will NOT be overwritten and will be re-saved. Any new or additional settings that the Setup Wizard finds on your website will be saved/setup.', 'bulletproof-security').'<br><br>'.__('When the Setup Wizard has completed you will see "The Setup Wizard has completed BPS Setup."', 'bulletproof-security').'<br><br>'.__('Your existing Root and wp-admin htaccess files are backed up before new Root and wp-admin htaccess files are created by the Setup Wizard. The BPS backup folder is here: ', 'bulletproof-security');
	echo $text;
	echo '/' . $bps_wpcontent_dir . '/bps-backup/master-backups/';
	$text = __(' and the backed up htaccess file names are: root.htaccess and wpadmin.htaccess.', 'bulletproof-security'); 
	echo $text;
	?>
    </td>
  </tr> 
</table> 
   
</div>

<?php
$text = '<span class="setup-wizard-inpage-text"><div class="setup-wizard-video-link" style="margin:15px 0px 20px 0px;"><a href="https://forum.ait-pro.com/video-tutorials/#setup-overview-free" target="_blank" title="This Setup Wizard link opens in a new Browser window">'.__('Setup Wizard & Overview Video Tutorial', 'bulletproof-security').'</a></div></span>';
echo $text;

bpsSetupWizardPrechecks();

?>

<form name="bpsSetupWizard" action="<?php echo admin_url( 'admin.php?page=bulletproof-security/admin/wizard/wizard.php' ); ?>" method="post">
	<?php wp_nonce_field('bps_setup_wizard'); ?>

<input type="submit" name="Submit-Setup-Wizard" style="margin:15px 0px 20px 0px;" value="<?php esc_attr_e('Setup Wizard', 'bulletproof-security') ?>" class="button bps-button" onclick="bpsSpinnerSWizard()" />
<?php bpsSetupWizard(); ?>
</form>

</td>
  </tr>
</table>

</div>
        
<div id="bps-tabs-2" class="bps-tab-page">

<?php bpsPro_hfiles_inpage_message(); ?>

<table width="100%" border="0" cellspacing="0" cellpadding="0" class="bps-help_faq_table">
  <tr>
    <td class="bps-table_title">
<?php $text = '<h2>'.__('Setup Wizard Options ~ ', 'bulletproof-security').'<span style="font-size:.75em;">'.__('Click the Setup Wizard Options Read Me help button for help info about each option setting', 'bulletproof-security').'</span></h2><div class="promo-text">'.__('Want even more security protection?', 'bulletproof-security').'<br>'.__('Protect all of your website files with AutoRestore|Quarantine Intrusion Detection & Prevention System: ', 'bulletproof-security').'<a href="https://affiliates.ait-pro.com/po/" target="_blank" title="BPS Pro ARQ IDPS">'.__('Get BPS Pro ARQ IDPS', 'bulletproof-security').'</a><br>'.__('Protect against SpamBot & HackerBot (auto-registering, auto-logins, auto-posting, auto-commenting): ', 'bulletproof-security').'<a href="https://affiliates.ait-pro.com/po/" target="_blank" title="BPS Pro JTC Anti-Spam|Anti-Hacker">'.__('Get BPS Pro JTC Anti-Spam|Anti-Hacker', 'bulletproof-security').'</a><br>'.__('Protect all of your Plugins (plugin folders and files) with an IP Firewall: ', 'bulletproof-security').'<a href="https://affiliates.ait-pro.com/po/" target="_blank" title="BPS Pro Plugin Firewall">'.__('Get BPS Pro Plugin Firewall', 'bulletproof-security').'</a><br>'.__('Protect your WordPress uploads folder against remote access or execution of files: ', 'bulletproof-security').'<a href="https://affiliates.ait-pro.com/po/" target="_blank" title="BPS Pro Uploads Anti-Exploit Guard">'.__('Get BPS Pro Uploads Anti-Exploit Guard', 'bulletproof-security').'</a></div>'; echo $text; ?>    
    </td>
  </tr>
  <tr>
    <td class="bps-table_cell_help">
    
<h3 style="margin:0px 0px 5px 0px;"><?php _e('Setup Wizard Options', 'bulletproof-security'); ?>  <button id="bps-open-modal2" class="button bps-modal-button"><?php _e('Read Me', 'bulletproof-security'); ?></button></h3>

<div id="bps-modal-content2" class="bps-dialog-hide" title="<?php _e('Setup Wizard Options', 'bulletproof-security'); ?>">
	
<table width="100%" border="0" cellspacing="0" cellpadding="0" class="bps-readme-table">
  <tr>
    <td class="bps-readme-table-td">	
	
	<?php $dialog_text = '<strong>'.__('This Read Me Help window is draggable (top) and resizable (bottom right corner)', 'bulletproof-security').'</strong><br><br><strong><font color="blue">'.__('Forum Help Links:', 'bulletproof-security').'</font></strong><br>';
		echo $dialog_text;
	?>
	
    <strong><a href="https://forum.ait-pro.com/forums/topic/gdmw/" title="Go Daddy Managed WordPress Hosting (GDMW)" target="_blank"><?php _e('Go Daddy Managed WordPress Hosting (GDMW)', 'bulletproof-security'); ?></a></strong><br />
    <strong><a href="https://forum.ait-pro.com/forums/topic/htaccess-files-disabled-setup-wizard-enable-disable-htaccess-files/" title="Enable|Disable htaccess Files" target="_blank"><?php _e('Enable|Disable htaccess Files', 'bulletproof-security'); ?></a></strong><br />
 	<strong><a href="https://forum.ait-pro.com/forums/topic/setup-wizard-autofix/" title="AutoFix" target="_blank"><?php _e('AutoFix Forum Topic', 'bulletproof-security'); ?></a></strong><br />
 	<strong><a href="https://forum.ait-pro.com/forums/topic/bps-gdpr-compliance/" title="GDPR Compliance" target="_blank"><?php _e('GDPR Compliance Forum Topic', 'bulletproof-security'); ?></a></strong><br /><br />
	
	<?php
    $dialog_text = '<strong>'.__('AutoFix (AutoWhitelist|AutoSetup|AutoCleanup)', 'bulletproof-security').'</strong><br>'.__('Setup Wizard AutoFix is turned On by default. When AutoFix is turned On the Setup Wizard will automatically create htaccess whitelist rules in BPS Custom Code and your Live htaccess files for other plugins and themes that you have installed that require htaccess code whitelist rules. Setup Wizard AutoFix will also automatically setup or cleanup htaccess code in BPS Custom Code for these caching plugins: WP Super Cache, W3 Total Cache, Comet Cache Plugin (free & Pro), WP Fastest Cache Plugin (free & Premium), Endurance Page Cache and WP Rocket. If a problem occurs with AutoFix you can turn On the AutoFix Debugger on the BPS UI|UX Settings page > BPS UI|UX|AutoFix Debug option to check the plugin or theme name and the BPS Custom Code text box where the problem is occurring. You can also turn Off AutoFix and AutoFix will not try to detect or create Custom Code whitelist rules or setup or cleanup caching plugins htaccess code. If a problem does occur with AutoFix turn On the BPS UI|UX|AutoFix Debug option, copy the AutoFix Debug information that is displayed to you and then click the AutoFix Forum Topic link at the top of this Read Me help window and post a forum Reply with your AutoFix Debug information so that we can figure out what the problem is.', 'bulletproof-security').'<br><br><strong>'.__('GDPR Compliance (IP Address Logging On|Off)', 'bulletproof-security').'</strong><br>'.__('The GDPR Compliance option setting is set to Off by default. Choosing the GDPR Compliance On option setting will disable IP address logging in all BPS features that log IP addresses. This plain text will be logged instead of IP addresses: GDPR Compliance On. List of BPS features that log IP addresses: Security Log, Login Security and Maintenance Mode. Note: For simplicity and ease of use this GDPR Compliance Setup Wizard Options setting is the only option setting that needs to be set instead of creating individual option settings in all BPS features that perform IP address logging. For more information about GDPR Compliance click the GDPR Compliance Forum Topic link at the top of this Read Me help window.', 'bulletproof-security').'<br><br><strong>'.__('Go Daddy Managed WordPress Hosting (GDMW):', 'bulletproof-security').'</strong><br>'.__('This option is ONLY for a special type of Go Daddy Hosting account called "Managed WordPress Hosting" and is NOT for regular/standard Go Daddy Hosting account types. Leave the default setting set to No, unless you have a Go Daddy Managed WordPress Hosting account. See the Forum Help Links section above for more information.', 'bulletproof-security').'<br><br><strong>'.__('Enable|Disable htaccess Files:', 'bulletproof-security').'</strong><br>'.__('Before changing this option setting, click the ', 'bulletproof-security').'<strong><font color="blue">'.__('Enable|Disable htaccess Files', 'bulletproof-security').'</font></strong>'.__(' Forum Help Link at the top of this Read Me help window to find out exactly what this option setting does and when it should or should not be used. htaccess Files Disabled: Will disable all BPS htaccess features and files. htaccess Files Enabled: Will enable all BPS htaccess freatures and files.', 'bulletproof-security').'<br><br><strong>'.__('Enable|Disable wp-admin BulletProof Mode', 'bulletproof-security').'</strong><br>'.__('The default setting is already set to: wp-admin BulletProof Mode Enabled. If you would like to disable wp-admin BulletProof Mode select wp-admin BulletProof Mode Disabled.', 'bulletproof-security').'<br><br><strong>'.__('Zip File Download Fix (Incapsula, Proxy, Other Cause):', 'bulletproof-security').'</strong><br>'.__('This option should only be set to On if you are seeing a 403 error and/or unable to download these Zip files: Custom Code Export Zip file, Login Security Table Export Zip file or the Setup Wizard Root htaccess file backup Zip file. The Setup Wizard Root htaccess file backup Zip file link is only displayed if BPS detects that your current Root htaccess file is not a BPS Root htaccess file. If you are still unable to download zip files after setting this option to On then you will need to whitelist your Proxy IP address in the Plugin Firewall Whitelist by Hostname (domain name) and IP Address tool under the Plugin Firewall Additional Whitelist Tools accordion tab. If that does not work then you will need to deactivate the Plugin Firewall temporarily, download the zip file and then activate the Plugin Firewall again.', 'bulletproof-security').'<br><br><strong>'.__('Multisite Hide|Display System Info Page for Subsites:', 'bulletproof-security').'</strong><br>'.__('This option is for Network|Multisite sites only. Choosing Hide System Info Page will hide the System Info menu link under the BPS navigational menus. Choosing Display System Info page will display the System Info menu link under the BPS navigational mensus.', 'bulletproof-security').'<br><br><strong>'.__('Network|Multisite Sitewide Login Security Settings', 'bulletproof-security').'</strong><br>'.__('This option is for Network|Multisite sites only. This is an independent option Form that creates and saves Login Security DB option settings for all Network sites when you click the Save Network LSM Options Sitewide button. If Login Security option settings have already been setup and saved for any Network site then those Login Security option settings will NOT be changed. If Login Security options settings have NOT already been setup and saved for any Network site then those Login Security option settings will be created and saved with these default settings: Max Login Attempts: 3, Automatic Lockout Time: 60, Manual Lockout Time: 60, Max DB Rows To Show: blank show all rows, Turn On|Turn Off: Turn On Login Security, Logging Options: Log Only Account Lockouts, Error Messages: Standard WP Login Errors, Attempts Remaining: Show Login Attempts Remaining, Password Reset: Enable Password Reset, Sort DB Rows: Ascending - Show Oldest Login First.', 'bulletproof-security').'<br><br><strong>'.__('Network|Multisite Sitewide JTC-Lite Settings', 'bulletproof-security').'</strong><br>'.__('This option is for Network|Multisite sites only. This is an independent option Form that creates and saves JTC-Lite DB option settings for all Network sites when you click the Save Network JTC Options Sitewide button. If JTC option settings have already been setup and saved for any Network site then those JTC option settings will not be changed. If JTC options settings have not already been setup and saved for any Network site then those JTC option settings will be created and saved with these default settings: JTC CAPTCHA: jtc, JTC ToolTip: Type/Enter: jtc, JTC Title|Text: Hover or click the text box below, Enable|Disable JTC Anti-Spam For These Forms: Login Form checkbox is checked and will display the JTC CAPTCHA text box on the Login Form.', 'bulletproof-security'); 
	echo $dialog_text; 
	?>

    </td>
  </tr> 
</table> 

</div>

<form name="AutoFix" action="options.php#bps-tabs-2" method="post">
	<?php settings_fields('bulletproof_security_options_wizard_autofix'); ?>
	<?php $AutoFix_Options = get_option('bulletproof_security_options_wizard_autofix'); ?>
	
    <strong><label for="auto-fix"><?php _e('AutoFix (AutoWhitelist|AutoSetup|AutoCleanup):', 'bulletproof-security'); ?></label></strong><br />
<select name="bulletproof_security_options_wizard_autofix[bps_wizard_autofix]" class="form-300" style="margin-top:5px;">
<option value="On" <?php selected('On', $AutoFix_Options['bps_wizard_autofix']); ?>><?php _e('AutoFix On', 'bulletproof-security'); ?></option>
<option value="Off" <?php selected('Off', $AutoFix_Options['bps_wizard_autofix']); ?>><?php _e('AutoFix Off', 'bulletproof-security'); ?></option>
</select><br />
<input type="submit" name="Submit-AutoFix" class="button bps-button" style="margin:10px 0px 20px 0px;width:202px;height:auto;white-space:normal" value="<?php esc_attr_e('Save AutoFix Option', 'bulletproof-security') ?>" />
</form>

<form name="GDPR" action="options.php#bps-tabs-2" method="post">
	<?php settings_fields('bulletproof_security_options_gdpr'); ?>
	<?php $GDPR_Options = get_option('bulletproof_security_options_gdpr'); ?>
	
    <strong><label for="gdpr"><?php _e('GDPR Compliance (IP Address Logging On|Off):', 'bulletproof-security'); ?></label></strong><br />
<select name="bulletproof_security_options_gdpr[bps_gdpr_on_off]" class="form-300" style="margin-top:5px;">
<option value="Off" <?php selected('Off', $GDPR_Options['bps_gdpr_on_off']); ?>><?php _e('GDPR Compliance Off', 'bulletproof-security'); ?></option>
<option value="On" <?php selected('On', $GDPR_Options['bps_gdpr_on_off']); ?>><?php _e('GDPR Compliance On', 'bulletproof-security'); ?></option>
</select><br />
<input type="submit" name="Submit-GDPR" class="button bps-button" style="margin:10px 0px 20px 0px;width:202px;height:auto;white-space:normal" value="<?php esc_attr_e('Save GDPR Option', 'bulletproof-security') ?>" />
</form>

<form name="SetupWizardGDMW" action="options.php#bps-tabs-2" method="post">
	<?php settings_fields('bulletproof_security_options_GDMW'); ?> 
	<?php $GDMWoptions = get_option('bulletproof_security_options_GDMW'); ?>
    
	<label for="wizard-curl"><?php _e('Go Daddy Managed WordPress Hosting (GDMW):', 'bulletproof-security'); ?></label><br />
<select name="bulletproof_security_options_GDMW[bps_gdmw_hosting]" class="form-300">
<option value="no" <?php selected('no', $GDMWoptions['bps_gdmw_hosting']); ?>><?php _e('No (default setting)', 'bulletproof-security'); ?></option>
<option value="yes" <?php selected('yes', $GDMWoptions['bps_gdmw_hosting']); ?>><?php _e('Yes (ONLY if you have Managed WordPress Hosting)', 'bulletproof-security'); ?></option>
</select><br />
<input type="submit" name="Submit-Wizard-GDMW" class="button bps-button" style="margin:10px 0px 20px 0px;width:202px;height:auto;white-space:normal" value="<?php esc_attr_e('Save GDMW Option', 'bulletproof-security') ?>" />
</form>    

 <form name="SetupWizardHFiles" action="options.php#bps-tabs-2" method="post">
	<?php settings_fields('bulletproof_security_options_htaccess_files'); ?> 
	<?php $HFiles_options = get_option('bulletproof_security_options_htaccess_files'); ?>
    
	<label for="wizard-curl"><?php _e('Enable|Disable htaccess Files:', 'bulletproof-security'); ?></label><br />
	<label for="wizard-curl" class="setup-wizard-blue-small-text" style="color:#2ea2cc;"><?php _e('CAUTION: Click the Read Me help button before changing this option setting', 'bulletproof-security'); ?></label><br />
<select name="bulletproof_security_options_htaccess_files[bps_htaccess_files]" class="form-300">
<option value="enabled" <?php selected('enabled', $HFiles_options['bps_htaccess_files']); ?>><?php _e('htaccess Files Enabled', 'bulletproof-security'); ?></option>
<option value="disabled" <?php selected('disabled', $HFiles_options['bps_htaccess_files']); ?>><?php _e('htaccess Files Disabled', 'bulletproof-security'); ?></option>
</select><br />
<input type="submit" name="Submit-Wizard-HFiles" class="button bps-button" style="margin:10px 0px 20px 0px;width:202px;height:auto;white-space:normal" value="<?php esc_attr_e('Enable|Disable', 'bulletproof-security') ?>" />
</form>  

<form name="wpadminEnableDisable" action="options.php#bps-tabs-2" method="post">
	<?php settings_fields('bulletproof_security_options_htaccess_res'); ?> 
	<?php $BPS_wpadmin_Options = get_option('bulletproof_security_options_htaccess_res'); ?>
	<strong><label for="wpadmin-res"><?php _e('Enable|Disable wp-admin BulletProof Mode:', 'bulletproof-security'); ?></label></strong><br />
<select name="bulletproof_security_options_htaccess_res[bps_wpadmin_restriction]" class="form-300" style="margin-top:5px;">
<option value="enabled" <?php selected('enabled', $BPS_wpadmin_Options['bps_wpadmin_restriction']); ?>><?php _e('wp-admin BulletProof Mode Enabled', 'bulletproof-security'); ?></option>
<option value="disabled" <?php selected('disabled', $BPS_wpadmin_Options['bps_wpadmin_restriction']); ?>><?php _e('wp-admin BulletProof Mode Disabled', 'bulletproof-security'); ?></option>
</select><br />
<input type="submit" name="Submit-Enable-Disable-wpadmin" class="button bps-button" style="margin:10px 0px 20px 0px;width:202px;height:auto;white-space:normal" value="<?php esc_attr_e('Enable|Disable', 'bulletproof-security') ?>" />
</form>

<form name="ZipDownloadFix" action="<?php echo admin_url( 'admin.php?page=bulletproof-security/admin/wizard/wizard.php#bps-tabs-2' ); ?>" method="post">
	<?php wp_nonce_field('bulletproof_security_zip_download_fix'); ?>
	<?php $Zip_download_Options = get_option('bulletproof_security_options_zip_fix'); ?>
	
    <strong><label for="zip-fix"><?php _e('Zip File Download Fix (Incapsula, Proxy, Other Cause):', 'bulletproof-security'); ?></label></strong><br />
<select name="bulletproof_security_options_zip_fix" class="form-300" style="margin-top:5px;">
<option value="Off" <?php selected('Off', $Zip_download_Options['bps_zip_download_fix']); ?>><?php _e('Zip File Download Fix Off', 'bulletproof-security'); ?></option>
<option value="On" <?php selected('On', $Zip_download_Options['bps_zip_download_fix']); ?>><?php _e('Zip File Download Fix On', 'bulletproof-security'); ?></option>
</select><br />
<input type="submit" name="Submit-Zip-Download-Fix" class="button bps-button" style="margin:10px 0px 20px 0px;width:232px;height:auto;white-space:normal" value="<?php esc_attr_e('Save Zip File Download Fix Option', 'bulletproof-security') ?>" />
</form>

<form name="muSysinfo" action="<?php echo admin_url( 'admin.php?page=bulletproof-security/admin/wizard/wizard.php#bps-tabs-2' ); ?>" method="post">
	<?php wp_nonce_field('bulletproof_security_options_mu_sysinfo'); ?>
	<?php $Mu_Sysinfo_page_options = get_option('bulletproof_security_options_mu_sysinfo'); ?>
	
    <strong><label for="mu-sysinfo"><?php _e('Multisite Hide|Display System Info Page for Subsites:', 'bulletproof-security'); ?></label></strong><br />
<select name="bulletproof_security_options_mu_sysinfo_select" class="form-300" style="margin-top:5px;">
<option value="display" <?php selected('display', $Mu_Sysinfo_page_options['bps_sysinfo_hide_display']); ?>><?php _e('Display System Info Page', 'bulletproof-security'); ?></option>
<option value="hide" <?php selected('hide', $Mu_Sysinfo_page_options['bps_sysinfo_hide_display']); ?>><?php _e('Hide System Info Page', 'bulletproof-security'); ?></option>
</select><br />
<input type="submit" name="Submit-MU-Sysinfo-Display" class="button bps-button" style="margin:10px 0px 20px 0px;width:232px;height:auto;white-space:normal" value="<?php esc_attr_e('Save Multisite Hide|Display Option', 'bulletproof-security') ?>" />
</form>

<form name="bpsNetLSM" action="<?php echo admin_url( 'admin.php?page=bulletproof-security/admin/wizard/wizard.php#bps-tabs-2' ); ?>" method="post">
<?php wp_nonce_field('bulletproof_security_net_lsm'); ?>
<div>
<strong><label for="NetLSM"><?php _e('Network|Multisite Sitewide Login Security Settings', 'bulletproof-security'); ?></label></strong><br />  
<input type="submit" name="Submit-Net-LSM" class="button bps-button" style="margin:10px 0px 20px 0px;width:232px;height:auto;white-space:normal" value="<?php esc_attr_e('Save Network LSM Options Sitewide', 'bulletproof-security') ?>" />
</div>
</form>

<form name="bpsNetJTC" action="<?php echo admin_url( 'admin.php?page=bulletproof-security/admin/wizard/wizard.php#bps-tabs-2' ); ?>" method="post">
<?php wp_nonce_field('bulletproof_security_net_jtc'); ?>
<div>
<strong><label for="NetLSM"><?php _e('Network|Multisite Sitewide JTC-Lite Settings', 'bulletproof-security'); ?></label></strong><br />  
<input type="submit" name="Submit-Net-JTC" class="button bps-button" style="margin:10px 0px 20px 0px;width:232px;height:auto;white-space:normal" value="<?php esc_attr_e('Save Network JTC Options Sitewide', 'bulletproof-security') ?>" />
</div>
</form>

<?php
// Zip File Download Fix
if ( isset( $_POST['Submit-Zip-Download-Fix'] ) && current_user_can('manage_options') ) {
		check_admin_referer( 'bulletproof_security_zip_download_fix' );
		
	if ( esc_html($_POST['bulletproof_security_options_zip_fix']) == 'On' ) {		
	
		$core_htaccess = WP_PLUGIN_DIR . '/bulletproof-security/admin/core/.htaccess';
		$login_htaccess = WP_PLUGIN_DIR . '/bulletproof-security/admin/login/.htaccess';
		$wizard_htaccess = WP_PLUGIN_DIR . '/bulletproof-security/admin/wizard/.htaccess';
	
		$files = array( $core_htaccess, $login_htaccess, $wizard_htaccess );
	
		foreach ( $files as $file ) {
			if ( file_exists($file) ) {
				unlink($file);
			}
		}
	
		$zip_fix_options = array( 'bps_zip_download_fix' => 'On' );

		foreach( $zip_fix_options as $key => $value ) {
			update_option('bulletproof_security_options_zip_fix', $zip_fix_options);
		}

		echo $bps_topDiv;
		$text = '<font color="green"><strong>'.__('The Zip File Download Fix option is set to On. This option should only be set to On if you are unable to download these Zip files: Custom Code Export Zip file, Login Security Table Export Zip file or the Setup Wizard Root htaccess file backup Zip file.', 'bulletproof-security').'</strong></font>';
		echo $text;
		echo $bps_bottomDiv;		

	} elseif ( esc_html($_POST['bulletproof_security_options_zip_fix']) == 'Off' ) {	
		
		$zip_fix_options = array( 'bps_zip_download_fix' => 'Off' );

		foreach( $zip_fix_options as $key => $value ) {
			update_option('bulletproof_security_options_zip_fix', $zip_fix_options);
		}

		echo $bps_topDiv;
		$text = '<font color="green"><strong>'.__('The Zip File Download Fix option is set to Off.', 'bulletproof-security').'</strong></font>';
		echo $text;
		echo $bps_bottomDiv;
	}
}

// Network|Multisite: Multisite Hide|Display System Info Page for Subsites
if ( isset( $_POST['Submit-MU-Sysinfo-Display'] ) && current_user_can('manage_options') ) {
		check_admin_referer( 'bulletproof_security_options_mu_sysinfo' );
		
	$network_ids = wp_get_sites();

	foreach ( $network_ids as $key => $value ) {
			
		$net_id = $value['blog_id'];

		$MU_Sysinfo_Options = array( 'bps_sysinfo_hide_display' => esc_html($_POST['bulletproof_security_options_mu_sysinfo_select']) );	
	
		foreach( $MU_Sysinfo_Options as $key => $value ) {
			update_blog_option( $net_id, 'bulletproof_security_options_mu_sysinfo', $MU_Sysinfo_Options);
		}		
	}

	echo $bps_topDiv;
	$text = '<font color="green"><strong>'.__('Multisite Hide|Display System Info Page for Subsites option saved.', 'bulletproof-security').'</strong></font>';
	echo $text;
	echo $bps_bottomDiv;
}

// Network|Multisite: update/save Login Security DB option settings for all sites
if ( isset( $_POST['Submit-Net-LSM'] ) && current_user_can('manage_options') ) {
		check_admin_referer( 'bulletproof_security_net_lsm' );

	if ( is_multisite() ) {
	
		if ( wp_is_large_network() ) {
			echo $bps_topDiv;
			$text = '<font color="#fb0101"><strong>'.__('Error: Your Network site exceeds the default WP criteria for a large network site. Either you have more than 10,000 users or more than 10,000 sites. Please post a new forum thread in the BPS plugin support forum on wordpress.org for assistance.', 'bulletproof-security').'</strong></font>';
			echo $text;
			echo $bps_bottomDiv;
		
		return;
		}

		$successMessage = __(' LSM DB Options created or updated Successfully!', 'bulletproof-security');
		$successTextBegin = '<font color="green"><strong>';
		$successTextEnd = '</strong></font><br>';

		$network_ids = wp_get_sites();

		foreach ( $network_ids as $key => $value ) {
			
			$net_id = $value['blog_id'];
		
			$bps_Net_lsm = 'bulletproof_security_options_login_security';
	
			$BPS_Net_LSM_Options = array(
			'bps_max_logins' 				=> '3', 
			'bps_lockout_duration' 			=> '15', 
			'bps_manual_lockout_duration' 	=> '60', 
			'bps_max_db_rows_display' 		=> '', 
			'bps_login_security_OnOff' 		=> 'On', 
			'bps_login_security_logging' 	=> 'logLockouts', 
			'bps_login_security_errors' 	=> 'wpErrors', 
			'bps_login_security_remaining' 	=> 'On', 
			'bps_login_security_pw_reset' 	=> 'enable',  
			'bps_login_security_sort' 		=> 'ascending', 
			'bps_enable_lsm_woocommerce' 	=> '' 
			);

			if ( ! get_blog_option( $net_id, $bps_Net_lsm ) ) {	
		
				foreach( $BPS_Net_LSM_Options as $key => $value ) {
					update_blog_option( $net_id, 'bulletproof_security_options_login_security', $BPS_Net_LSM_Options );
				}
	
				echo $successTextBegin.'Site: '.$net_id.$successMessage.$successTextEnd;
			
			} else {

				$BPS_LSM_Options_Net = get_blog_option( $net_id, 'bulletproof_security_options_login_security' );
		
				$BPS_Net_Options_lsm = array(
				'bps_max_logins' 				=> $BPS_LSM_Options_Net['bps_max_logins'], 
				'bps_lockout_duration' 			=> $BPS_LSM_Options_Net['bps_lockout_duration'], 
				'bps_manual_lockout_duration' 	=> $BPS_LSM_Options_Net['bps_manual_lockout_duration'], 
				'bps_max_db_rows_display' 		=> $BPS_LSM_Options_Net['bps_max_db_rows_display'], 
				'bps_login_security_OnOff' 		=> $BPS_LSM_Options_Net['bps_login_security_OnOff'], 
				'bps_login_security_logging' 	=> $BPS_LSM_Options_Net['bps_login_security_logging'], 
				'bps_login_security_errors' 	=> $BPS_LSM_Options_Net['bps_login_security_errors'], 
				'bps_login_security_remaining' 	=> $BPS_LSM_Options_Net['bps_login_security_remaining'], 
				'bps_login_security_pw_reset' 	=> $BPS_LSM_Options_Net['bps_login_security_pw_reset'],  
				'bps_login_security_sort' 		=> $BPS_LSM_Options_Net['bps_login_security_sort'], 
				'bps_enable_lsm_woocommerce' 	=> '' 
				);

				foreach( $BPS_Net_Options_lsm as $key => $value ) {
					update_blog_option( $net_id, 'bulletproof_security_options_login_security', $BPS_Net_Options_lsm );
				}
			
					echo $successTextBegin.'Site: '.$net_id.$successMessage.$successTextEnd;
			}
		}
	}
}

// Network|Multisite: update/save JTC-Lite DB option settings for all sites
if ( isset( $_POST['Submit-Net-JTC'] ) && current_user_can('manage_options') ) {
		check_admin_referer( 'bulletproof_security_net_jtc' );

	if ( is_multisite() ) {
	
		if ( wp_is_large_network() ) {
			echo $bps_topDiv;
			$text = '<font color="#fb0101"><strong>'.__('Error: Your Network site exceeds the default WP criteria for a large network site. Either you have more than 10,000 users or more than 10,000 sites. Please send an email to info@ait-pro.com for help. Use this email Subject line: Setup Wizard Options Large Network Site Help.', 'bulletproof-security').'</strong></font>';
			echo $text;
			echo $bps_bottomDiv;
		
		return;
		}

		$successMessage = __(' JTC DB Options created or updated Successfully!', 'bulletproof-security');
		$successTextBegin = '<font color="green"><strong>';
		$successTextEnd = '</strong></font><br>';

		$network_ids = wp_get_sites();

		foreach ( $network_ids as $key => $value ) {
			
			$net_id = $value['blog_id'];
		
			$bps_Net_jtc = 'bulletproof_security_options_login_security_jtc';
	
			$BPS_Net_JTC_Options = array(
			'bps_tooltip_captcha_key' 			=> 'jtc', 
			'bps_tooltip_captcha_hover_text' 	=> 'Type/Enter:  jtc', 
			'bps_tooltip_captcha_title' 		=> 'Hover or click the text box below', 
			'bps_tooltip_captcha_logging' 		=> 'Off', 
			'bps_jtc_login_form' 				=> '1', 
			'bps_jtc_register_form' 			=> '', 
			'bps_jtc_lostpassword_form' 		=> '', 
			'bps_jtc_comment_form' 				=> '', 
			'bps_jtc_mu_register_form' 			=> '', 	
			'bps_jtc_buddypress_register_form' 	=> '', 
			'bps_jtc_buddypress_sidebar_form' 	=> '', 
			'bps_jtc_administrator' 			=> '', 
			'bps_jtc_editor' 					=> '', 
			'bps_jtc_author' 					=> '', 
			'bps_jtc_contributor' 				=> '', 
			'bps_jtc_subscriber' 				=> '', 
			'bps_jtc_comment_form_error' 		=> '', 
			'bps_jtc_comment_form_label' 		=> '', 
			'bps_jtc_comment_form_input' 		=> '', 
			'bps_jtc_custom_roles' 				=> '', 
			'bps_enable_jtc_woocommerce' 		=> '', 
			'bps_jtc_custom_form_error' 		=> '' 
			);

			if ( ! get_blog_option( $net_id, $bps_Net_jtc ) ) {	
		
				foreach( $BPS_Net_JTC_Options as $key => $value ) {
					update_blog_option( $net_id, 'bulletproof_security_options_login_security_jtc', $BPS_Net_JTC_Options );
				}
	
				echo $successTextBegin.'Site: '.$net_id.$successMessage.$successTextEnd;

			} else {

				$BPS_JTC_Options_Net = get_blog_option( $net_id, 'bulletproof_security_options_login_security_jtc' );
		
				$BPS_Net_Options_jtc = array(
				'bps_tooltip_captcha_key' 			=> $BPS_JTC_Options_Net['bps_tooltip_captcha_key'], 
				'bps_tooltip_captcha_hover_text' 	=> $BPS_JTC_Options_Net['bps_tooltip_captcha_hover_text'], 
				'bps_tooltip_captcha_title' 		=> $BPS_JTC_Options_Net['bps_tooltip_captcha_title'], 
				'bps_tooltip_captcha_logging' 		=> 'Off', 
				'bps_jtc_login_form' 				=> $BPS_JTC_Options_Net['bps_jtc_login_form'], 
				'bps_jtc_register_form' 			=> '', 
				'bps_jtc_lostpassword_form' 		=> '', 
				'bps_jtc_comment_form' 				=> '', 
				'bps_jtc_mu_register_form' 			=> '', 
				'bps_jtc_buddypress_register_form' 	=> '', 
				'bps_jtc_buddypress_sidebar_form' 	=> '', 
				'bps_jtc_administrator' 			=> '', 
				'bps_jtc_editor' 					=> '', 
				'bps_jtc_author' 					=> '', 
				'bps_jtc_contributor' 				=> '', 
				'bps_jtc_subscriber' 				=> '', 
				'bps_jtc_comment_form_error' 		=> $BPS_JTC_Options_Net['bps_jtc_comment_form_error'], 
				'bps_jtc_comment_form_label' 		=> $BPS_JTC_Options_Net['bps_jtc_comment_form_label'], 
				'bps_jtc_comment_form_input' 		=> $BPS_JTC_Options_Net['bps_jtc_comment_form_input'], 
				'bps_jtc_custom_roles' 				=> $BPS_JTC_Options_Net['bps_jtc_custom_roles'], 
				'bps_enable_jtc_woocommerce' 		=> '', 
				'bps_jtc_custom_form_error' 		=> $BPS_JTC_Options_Net['bps_jtc_custom_form_error'] 
				);

				foreach( $BPS_Net_Options_jtc as $key => $value ) {
					update_blog_option( $net_id, 'bulletproof_security_options_login_security_jtc', $BPS_Net_Options_jtc );
				}
					echo $successTextBegin.'Site: '.$net_id.$successMessage.$successTextEnd;
			}
		}
	}
}

?>

	</td>
  </tr>
</table>

</div>    

<div id="AITpro-link">BulletProof Security <?php echo BULLETPROOF_VERSION; ?> Plugin by <a href="https://forum.ait-pro.com/" target="_blank" title="AITpro Website Security">AITpro Website Security</a>
</div>
</div>
<style>
<!--
.bps-spinner {visibility:hidden;}
-->
</style>
</div>