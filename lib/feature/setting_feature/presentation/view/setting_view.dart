import 'package:cyper_shield_jo/feature/setting_feature/presentation/view/widgets/section_title.dart';
import 'package:cyper_shield_jo/feature/setting_feature/presentation/view/widgets/tile.dart';
import 'package:cyper_shield_jo/l10n/app_localizations.dart';
import 'package:cyper_shield_jo/main.dart';
import 'package:flutter/material.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  bool communityAlerts = true;
  bool smartScan = true;
  bool darkMode = false;
  String language = "Arabic";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(AppLocalizations.of(context)?.settings ?? "Settings"),
        centerTitle: true,
      ),
      body: ListView(
        children: [
          /// 🔹 Account & Profile
          sectionTitle(
            AppLocalizations.of(context)?.accountAndProfile ??
                "Account & Profile",
          ),
          tile(
            icon: Icons.person,
            title: AppLocalizations.of(context)?.myProfile ?? "My Profile",
            onTap: () {},
          ),
          tile(
            icon: Icons.lock,
            title:
                AppLocalizations.of(context)?.accountSecurity ??
                "Account Security",
            onTap: () {},
          ),

          /// Security & Notifications
          sectionTitle(
            AppLocalizations.of(context)?.securityAndNotifications ??
                "Security & Notifications",
          ),
          SwitchListTile(
            title: Text(
              AppLocalizations.of(context)?.communityAlerts ??
                  "Community Alerts",
            ),
            subtitle: Text(
              AppLocalizations.of(context)?.getAlertsForThreatsInJordan ??
                  "Get alerts for threats in Jordan",
            ),
            value: communityAlerts,
            onChanged: (val) {
              setState(() => communityAlerts = val);
            },
          ),
          SwitchListTile(
            title: Text(
              AppLocalizations.of(context)?.smartScan ?? "Smart Scan",
            ),
            subtitle: Text(
              AppLocalizations.of(context)?.autoScanCopiedLinks ??
                  "Auto scan copied links",
            ),
            value: smartScan,
            onChanged: (val) {
              setState(() => smartScan = val);
            },
          ),

          /// App Preferences
          sectionTitle(
            AppLocalizations.of(context)?.appPreferences ?? "App Preferences",
          ),
          ListTile(
            leading: const Icon(Icons.language),
            title: Text(AppLocalizations.of(context)?.language ?? "test"),
            subtitle: Text(language),
            onTap: () {
              _showLanguageDialog();
            },
          ),
          SwitchListTile(
            title: Text(AppLocalizations.of(context)?.darkMode ?? "Dark Mode"),
            value: darkMode,
            onChanged: (val) {
              setState(() => darkMode = val);
            },
          ),

          /// Privacy & Support
          sectionTitle(
            AppLocalizations.of(context)?.privacyAndSupport ??
                "Privacy & Support",
          ),
          ListTile(
            leading: const Icon(Icons.history),
            title: Text(
              AppLocalizations.of(context)?.scanHistory ?? "Scan History",
            ),
            onTap: () {},
          ),
          ListTile(
            leading: const Icon(Icons.privacy_tip),
            title: Text(
              AppLocalizations.of(context)?.privacyPolicy ?? "Privacy Policy",
            ),
            onTap: () {},
          ),
          ListTile(
            leading: const Icon(Icons.support),
            title: Text(AppLocalizations.of(context)?.support ?? "Support"),
            onTap: () {},
          ),
        ],
      ),
    );
  }

  ///  Language Dialog
  void _showLanguageDialog() {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text(
            AppLocalizations.of(context)?.chooseLanguage ?? "Choose Language",
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              RadioListTile(
                title: Text(AppLocalizations.of(context)?.arabic ?? "Arabic"),
                value: "Arabic",
                groupValue: language,
                onChanged: (val) {
                  setState(() => language = val!);
                  MyApp.setLocale(context, const Locale('ar'));
                  Navigator.pop(context);
                },
              ),
              RadioListTile(
                title: Text(AppLocalizations.of(context)?.english ?? "English"),
                value: "English",
                groupValue: language,
                onChanged: (val) {
                  setState(() => language = val!);
                  MyApp.setLocale(context, const Locale('en'));
                  Navigator.pop(context);
                },
              ),
            ],
          ),
        );
      },
    );
  }
}
