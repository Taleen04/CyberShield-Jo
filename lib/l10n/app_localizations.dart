import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_ar.dart';
import 'app_localizations_en.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'l10n/app_localizations.dart';
///
/// return MaterialApp(
///   localizationsDelegates: AppLocalizations.localizationsDelegates,
///   supportedLocales: AppLocalizations.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```yaml
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # Rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the AppLocalizations.supportedLocales
/// property.
abstract class AppLocalizations {
  AppLocalizations(String locale)
    : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates =
      <LocalizationsDelegate<dynamic>>[
        delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
      ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('ar'),
    Locale('en'),
  ];

  /// No description provided for @login.
  ///
  /// In en, this message translates to:
  /// **'Login'**
  String get login;

  /// No description provided for @welcome.
  ///
  /// In en, this message translates to:
  /// **'Welcome'**
  String get welcome;

  /// No description provided for @settings.
  ///
  /// In en, this message translates to:
  /// **'Settings'**
  String get settings;

  /// No description provided for @accountAndProfile.
  ///
  /// In en, this message translates to:
  /// **'Account & Profile'**
  String get accountAndProfile;

  /// No description provided for @myProfile.
  ///
  /// In en, this message translates to:
  /// **'My Profile'**
  String get myProfile;

  /// No description provided for @accountSecurity.
  ///
  /// In en, this message translates to:
  /// **'Account Security'**
  String get accountSecurity;

  /// No description provided for @securityAndNotifications.
  ///
  /// In en, this message translates to:
  /// **'Security & Notifications'**
  String get securityAndNotifications;

  /// No description provided for @communityAlerts.
  ///
  /// In en, this message translates to:
  /// **'Community Alerts'**
  String get communityAlerts;

  /// No description provided for @getAlertsForThreatsInJordan.
  ///
  /// In en, this message translates to:
  /// **'Get alerts for threats in Jordan'**
  String get getAlertsForThreatsInJordan;

  /// No description provided for @smartScan.
  ///
  /// In en, this message translates to:
  /// **'Smart Scan'**
  String get smartScan;

  /// No description provided for @autoScanCopiedLinks.
  ///
  /// In en, this message translates to:
  /// **'Auto scan copied links'**
  String get autoScanCopiedLinks;

  /// No description provided for @appPreferences.
  ///
  /// In en, this message translates to:
  /// **'App Preferences'**
  String get appPreferences;

  /// No description provided for @language.
  ///
  /// In en, this message translates to:
  /// **'Language'**
  String get language;

  /// No description provided for @chooseLanguage.
  ///
  /// In en, this message translates to:
  /// **'Choose Language'**
  String get chooseLanguage;

  /// No description provided for @arabic.
  ///
  /// In en, this message translates to:
  /// **'Arabic'**
  String get arabic;

  /// No description provided for @english.
  ///
  /// In en, this message translates to:
  /// **'English'**
  String get english;

  /// No description provided for @darkMode.
  ///
  /// In en, this message translates to:
  /// **'Dark Mode'**
  String get darkMode;

  /// No description provided for @privacyAndSupport.
  ///
  /// In en, this message translates to:
  /// **'Privacy & Support'**
  String get privacyAndSupport;

  /// No description provided for @scanHistory.
  ///
  /// In en, this message translates to:
  /// **'Scan History'**
  String get scanHistory;

  /// No description provided for @privacyPolicy.
  ///
  /// In en, this message translates to:
  /// **'Privacy Policy'**
  String get privacyPolicy;

  /// No description provided for @support.
  ///
  /// In en, this message translates to:
  /// **'Support'**
  String get support;

  /// No description provided for @analyzeContent.
  ///
  /// In en, this message translates to:
  /// **'Analyze Content'**
  String get analyzeContent;

  /// No description provided for @enterTextOrLink.
  ///
  /// In en, this message translates to:
  /// **'Enter text or link here'**
  String get enterTextOrLink;

  /// No description provided for @pasteLink.
  ///
  /// In en, this message translates to:
  /// **'Paste link here'**
  String get pasteLink;

  /// No description provided for @pasteText.
  ///
  /// In en, this message translates to:
  /// **'Paste text here'**
  String get pasteText;

  /// No description provided for @privacyNote.
  ///
  /// In en, this message translates to:
  /// **'Privacy Note'**
  String get privacyNote;

  /// No description provided for @privacyNoteBody.
  ///
  /// In en, this message translates to:
  /// **'We take your privacy seriously. No entered data is stored in the app. Content is analyzed anonymously for threat detection purposes only.'**
  String get privacyNoteBody;

  /// No description provided for @analyze.
  ///
  /// In en, this message translates to:
  /// **'Analyze'**
  String get analyze;

  /// No description provided for @recentChecks.
  ///
  /// In en, this message translates to:
  /// **'Recent Checks'**
  String get recentChecks;

  /// No description provided for @noRecentChecks.
  ///
  /// In en, this message translates to:
  /// **'No recent checks'**
  String get noRecentChecks;

  /// No description provided for @clearAll.
  ///
  /// In en, this message translates to:
  /// **'Clear All'**
  String get clearAll;

  /// No description provided for @report.
  ///
  /// In en, this message translates to:
  /// **'Report'**
  String get report;

  /// No description provided for @share.
  ///
  /// In en, this message translates to:
  /// **'Share'**
  String get share;

  /// No description provided for @call.
  ///
  /// In en, this message translates to:
  /// **'Call'**
  String get call;

  /// No description provided for @callNumber.
  ///
  /// In en, this message translates to:
  /// **'83838388'**
  String get callNumber;

  /// No description provided for @highRiskDetected.
  ///
  /// In en, this message translates to:
  /// **'High Risk Detected'**
  String get highRiskDetected;

  /// No description provided for @mediumRiskDetected.
  ///
  /// In en, this message translates to:
  /// **'Medium Risk Detected'**
  String get mediumRiskDetected;

  /// No description provided for @lowRiskDetected.
  ///
  /// In en, this message translates to:
  /// **'Low Risk Detected'**
  String get lowRiskDetected;

  /// No description provided for @scam.
  ///
  /// In en, this message translates to:
  /// **'Scam'**
  String get scam;

  /// No description provided for @phishing.
  ///
  /// In en, this message translates to:
  /// **'Phishing'**
  String get phishing;

  /// No description provided for @appearsSafe.
  ///
  /// In en, this message translates to:
  /// **'Appears Safe'**
  String get appearsSafe;

  /// No description provided for @explanation.
  ///
  /// In en, this message translates to:
  /// **'Explanation: '**
  String get explanation;

  /// No description provided for @reportScam.
  ///
  /// In en, this message translates to:
  /// **'Report Scam'**
  String get reportScam;

  /// No description provided for @shareResult.
  ///
  /// In en, this message translates to:
  /// **'Share Result'**
  String get shareResult;

  /// No description provided for @SMS.
  ///
  /// In en, this message translates to:
  /// **'SMS'**
  String get SMS;

  /// No description provided for @URL.
  ///
  /// In en, this message translates to:
  /// **'URL'**
  String get URL;

  /// No description provided for @Text.
  ///
  /// In en, this message translates to:
  /// **'Text'**
  String get Text;

  /// No description provided for @Phone.
  ///
  /// In en, this message translates to:
  /// **'Phone'**
  String get Phone;

  /// No description provided for @Explanation.
  ///
  /// In en, this message translates to:
  /// **'Explanation: '**
  String get Explanation;

  /// No description provided for @myReports.
  ///
  /// In en, this message translates to:
  /// **'My Reports'**
  String get myReports;

  /// No description provided for @underReview.
  ///
  /// In en, this message translates to:
  /// **'Under Review'**
  String get underReview;

  /// No description provided for @home.
  ///
  /// In en, this message translates to:
  /// **'Home'**
  String get home;

  /// No description provided for @reports.
  ///
  /// In en, this message translates to:
  /// **'Reports'**
  String get reports;
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(lookupAppLocalizations(locale));
  }

  @override
  bool isSupported(Locale locale) =>
      <String>['ar', 'en'].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {
  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'ar':
      return AppLocalizationsAr();
    case 'en':
      return AppLocalizationsEn();
  }

  throw FlutterError(
    'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
    'an issue with the localizations generation tool. Please file an issue '
    'on GitHub with a reproducible sample app and the gen-l10n configuration '
    'that was used.',
  );
}
