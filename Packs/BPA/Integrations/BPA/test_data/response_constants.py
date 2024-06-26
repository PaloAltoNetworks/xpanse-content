GET_RESULTS_RESPONSE = {
    "status": "complete",
    "results": {
        "version": "5.0.0",
        "adoption": ["adoption"],
        "adoption_summary": ["adoption summary"],
        "adoption_grand_totals": {"adoption grand totals": "stats"},
        "adoption_trend": ['adoption trend'],
        "bpa": {
            "network": {
                "ip_sec_crypto_profile": [
                    {
                        "configuration": {
                            "template_name": None,
                            "name": "default",
                            "protocol": "esp",
                            "encryption_algorithms": [
                                "aes-128-cbc",
                                "3des"
                            ],
                            "authentication_algorithms": [
                                "sha1"
                            ]
                        },
                        "warnings": [
                            {
                                "check_id": 84,
                                "check_name": "IPSec Crypto Profile Authentication",
                                "check_type": "Warning",
                                "check_message": "Recommended to only use SHA256 or higher for authentication. Please remove the following: sha1",
                                "check_passed": False
                            },
                            {
                                "check_id": 83,
                                "check_name": "IPSec Crypto Profile Encryption",
                                "check_type": "Warning",
                                "check_message": "Recommended to only use aes-128-gcm or aes-256-gcm for encryption. Please remove the following: aes-128-cbc, 3des",
                                "check_passed": False
                            },
                            {
                                "check_id": 82,
                                "check_name": "IPSec Crypto Profile Protocol",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": True
                            }
                        ],
                        "notes": []
                    },
                    {
                        "configuration": {
                            "template_name": None,
                            "name": "Suite-B-GCM-128",
                            "protocol": "esp",
                            "encryption_algorithms": [
                                "aes-128-gcm"
                            ],
                            "authentication_algorithms": []
                        },
                        "warnings": [
                            {
                                "check_id": 84,
                                "check_name": "IPSec Crypto Profile Authentication",
                                "check_type": "Warning",
                                "check_message": "Recommended to use SHA for authentication.",
                                "check_passed": False
                            },
                            {
                                "check_id": 83,
                                "check_name": "IPSec Crypto Profile Encryption",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": True
                            },
                            {
                                "check_id": 82,
                                "check_name": "IPSec Crypto Profile Protocol",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": True
                            }
                        ],
                        "notes": []
                    },
                    {
                        "configuration": {
                            "template_name": None,
                            "name": "Suite-B-GCM-256",
                            "protocol": "esp",
                            "encryption_algorithms": [
                                "aes-256-gcm"
                            ],
                            "authentication_algorithms": []
                        },
                        "warnings": [
                            {
                                "check_id": 84,
                                "check_name": "IPSec Crypto Profile Authentication",
                                "check_type": "Warning",
                                "check_message": "Recommended to use SHA for authentication.",
                                "check_passed": False
                            },
                            {
                                "check_id": 83,
                                "check_name": "IPSec Crypto Profile Encryption",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": True
                            },
                            {
                                "check_id": 82,
                                "check_name": "IPSec Crypto Profile Protocol",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": True
                            }
                        ],
                        "notes": []
                    }
                ],
                "interface_management_profile": [],
                "gre_tunnel": [],
                "zone_protection_profile": [],
                "global_protect_gateway": [],
                "global_protect_portal": [],
                "zone": []
            },
            "policies": {
                "app_override": [],
                "security_rule": [
                    {
                        "configuration": {
                            "location": "vsys1",
                            "rule_enabled": True,
                            "rule_name": "demisto-de120a54",
                            "rule_uuid": "d0a77816-b30a-4cae-b8fa-a21770a1ceb8",
                            "rule_type": "universal",
                            "rulebase": "rulebase",
                            "action": "deny",
                            "description": "labala",
                            "schedule": "",
                            "disable_server_response_inspection_enabled": False,
                            "applications": [
                                "backweb"
                            ],
                            "hip_profiles": [
                                "any"
                            ],
                            "services": [
                                "any"
                            ],
                            "url_categories": [
                                "any"
                            ],
                            "tags": [],
                            "targets": [
                                "007051000065136:vsys1"
                            ],
                            "log_end_enabled": True,
                            "log_forwarding_profile": "none",
                            "log_start_enabled": False,
                            "source_addresses": [
                                "any"
                            ],
                            "source_users": [
                                "any"
                            ],
                            "source_zones": [
                                "any"
                            ],
                            "dest_addresses": [
                                "any"
                            ],
                            "dest_zones": [
                                "any"
                            ],
                            "profile_antivirus": None,
                            "profile_anti_spyware": "strict",
                            "profile_vulnerability_protection": None,
                            "profile_url_filtering": "url_filter_test_pb_pano",
                            "profile_file_blocking": None,
                            "profile_wildfire_analysis": None,
                            "profile_data_filtering": None,
                            "profile_group": "test_group_profile"
                        },
                        "warnings": [
                            {
                                "check_id": 220,
                                "check_name": "APP-ID with Service",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": None,
                                "check_excluded": True
                            },
                            {
                                "check_id": 208,
                                "check_name": "Application != any",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": None,
                                "check_excluded": True
                            },
                            {
                                "check_id": 3,
                                "check_name": "Description Populated",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": True,
                                "check_excluded": False
                            },
                            {
                                "check_id": 9,
                                "check_name": "Disable Server Response Inspection",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": True,
                                "check_excluded": False
                            },
                            {
                                "check_id": 8,
                                "check_name": "Expired Non-Recurring Schedules",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": True,
                                "check_excluded": False
                            },
                            {
                                "check_id": 7,
                                "check_name": "Log Forwarding",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": False,
                                "check_excluded": False
                            },
                            {
                                "check_id": 6,
                                "check_name": "Log at Start of Session",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": True,
                                "check_excluded": False
                            },
                            {
                                "check_id": 5,
                                "check_name": "Service != any",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": True,
                                "check_excluded": False
                            },
                            {
                                "check_id": 4,
                                "check_name": "Source/Destination = any/any",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": True,
                                "check_excluded": False
                            }
                        ],
                        "notes": []
                    }
                ],
                "decryption_rulebase": [
                    {
                        "configuration": {
                            "location": "vsys1",
                            "ssh_proxy_decrypt_rule_exists": False,
                            "ssh_security_allow_rule_exists": False,
                            "ssh_tunnel_security_deny_rule_exists": False,
                            "decryption_rules": False,
                            "security_rules": True
                        },
                        "warnings": [
                            {
                                "check_id": 20,
                                "check_name": "SSH Proxy / SSH Tunnel",
                                "check_type": "Warning",
                                "check_message": "It is recommended to configure SSH Proxy to detect and block SSH Tunneling and to limit user access to SSH traffic",
                                "check_passed": False
                            }
                        ],
                        "notes": []
                    }
                ],
                "security_rulebase": [
                    {
                        "configuration": {
                            "security_rules": [
                                {
                                    "location": "vsys1",
                                    "rule_enabled": True,
                                    "rule_name": "demisto-de120a54",
                                    "rule_uuid": "d0a77816-b30a-4cae-b8fa-a21770a1ceb8",
                                    "rule_type": "universal",
                                    "rulebase": "rulebase",
                                    "action": "deny",
                                    "description": "labala",
                                    "schedule": "",
                                    "disable_server_response_inspection_enabled": False,
                                    "applications": [
                                        "backweb"
                                    ],
                                    "hip_profiles": [
                                        "any"
                                    ],
                                    "services": [
                                        "any"
                                    ],
                                    "url_categories": [
                                        "any"
                                    ],
                                    "tags": [],
                                    "targets": [
                                        "007051000065136:vsys1"
                                    ],
                                    "log_end_enabled": True,
                                    "log_forwarding_profile": "none",
                                    "log_start_enabled": False,
                                    "source_addresses": [
                                        "any"
                                    ],
                                    "source_users": [
                                        "any"
                                    ],
                                    "source_zones": [
                                        "any"
                                    ],
                                    "dest_addresses": [
                                        "any"
                                    ],
                                    "dest_zones": [
                                        "any"
                                    ],
                                    "profile_antivirus": None,
                                    "profile_anti_spyware": "strict",
                                    "profile_vulnerability_protection": None,
                                    "profile_url_filtering": "url_filter_test_pb_pano",
                                    "profile_file_blocking": None,
                                    "profile_wildfire_analysis": None,
                                    "profile_data_filtering": None,
                                    "profile_group": "test_group_profile"
                                }
                            ],
                            "location": "vsys1"
                        },
                        "warnings": [
                            {
                                "check_id": 11,
                                "check_name": "Disabled Rules",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": True
                            },
                            {
                                "check_id": 12,
                                "check_name": "Interzone Deny Rule with Logging",
                                "check_type": "Warning",
                                "check_message": "It is recommended to override the interzone-default rule with any Action except 'allow' and Log at Session End enabled.",
                                "check_passed": False
                            },
                            {
                                "check_id": 13,
                                "check_name": "Intrazone Allow Rules with Logging",
                                "check_type": "Warning",
                                "check_message": "It is recommended to override the intrazone-default rule with Action set to 'allow', Log at Session End enabled, and IPS capability enabled.",
                                "check_passed": False
                            },
                            {
                                "check_id": 249,
                                "check_name": "New Apps with Application Filter",
                                "check_type": "Warning",
                                "check_message": "Configure a security rule with an action of allow and an application filter with \"new App-IDs only\" enabled to ensure business critical applications function as expected",
                                "check_passed": False
                            },
                            {
                                "check_id": 261,
                                "check_name": "Inbound Malicious IP Address Feed",
                                "check_type": "Warning",
                                "check_message": "It is recommended to configure and enable a deny rule with the 'Palo Alto Networks - Known malicious IP addresses' EDL in the source address, Log at Session End enabled, and a Log Forwarding Profile configured",
                                "check_passed": False
                            },
                            {
                                "check_id": 262,
                                "check_name": "Outbound Malicious IP Address Feed",
                                "check_type": "Warning",
                                "check_message": "It is recommended to configure and enable a deny rule with the 'Palo Alto Networks - Known malicious IP addresses' EDL in the destination address, Log at Session End enabled, and a Log Forwarding Profile configured",
                                "check_passed": False
                            },
                            {
                                "check_id": 241,
                                "check_name": "Quic App Deny Rule",
                                "check_type": "Warning",
                                "check_message": "It is recommended to have a security rule with application = 'quic' and action != 'allow' before any allow rules to ensure encrypted traffic is decrypted and inspected",
                                "check_passed": False
                            },
                            {
                                "check_id": 15,
                                "check_name": "HIP Profiles used in Rules",
                                "check_type": "Warning",
                                "check_message": None,
                                "check_passed": True
                            }
                        ],
                        "notes": [
                            {
                                "check_id": 263,
                                "check_name": "Inbound High Risk IP Address Feed",
                                "check_type": "Note",
                                "check_message": "It is recommended to configure and enable a deny rule with\n                    the 'Palo Alto Networks - High risk IP addresses' EDL in the source address,\n                    Log at Session End enabled, and a Log Forwarding Profile configured\n                    OR an allow rule with the same configurations along with Antivirus, Vulnerablility Protection,\n                    Anti-Spyware and URL Filtering profiles configured",
                                "check_severity": "Caution"
                            },
                            {
                                "check_id": 264,
                                "check_name": "Outbound High Risk IP Address Feed",
                                "check_type": "Note",
                                "check_message": "It is recommended to configure and enable a deny rule with\n                    the 'Palo Alto Networks - High risk IP addresses' EDL in the destination address,\n                    Log at Session End enabled, and a Log Forwarding Profile configured\n                    OR an allow rule with the same configurations along with Antivirus, Vulnerablility Protection,\n                    Anti-Spyware and URL Filtering profiles configured",
                                "check_severity": "Caution"
                            }
                        ]
                    }
                ],
                "policy_based_forwarding_rule": [],
                "captive_portal_rule": [],
                "dos_protection_rule": [],
                "decryption_rule": [],
                "tunnel_inspection": []
            }
        },
        "bpa_checks_grand_total": {"bpa checks grand total": "stats"},
        "timestamp": "2020-12-23T14:27:18.579769Z"
    }
}

GET_DOCUMENTATION_RESPONSE = [
    {
        "doc_id": 3,
        "top_nav": "Policies",
        "left_nav": "Security",
        "title": "Description Populated",
        "doc_type": "Warning",
        "description": "Create a description for the rule.",
        "rationale": "As the Security policy rulebase grows and becomes more granular, the Description helps to differentiate and provide context for each rule.",
        "references": "['https://www.paloaltonetworks.com/documentation/81/pan-os/pan-os/policy/security-policy/components-of-a-security-policy-rule']",
        "active": True,
        "last_updated_date": "2020-10-05T22:46:57.579074Z",
        "capability_label": [
            "Corrective"
        ],
        "class_label": [
            "Operational"
        ],
        "control_category": [
            "Configuration Management"
        ],
        "cscv6_control": [],
        "cscv7_control": [],
        "complexity": "Easy",
        "effort": 5
    },
    {
        "doc_id": 4,
        "top_nav": "Policies",
        "left_nav": "Security",
        "title": "Source/Destination = any/any",
        "doc_type": "Warning",
        "description": "Do not specify both the source and destination zones as \"any\" on the rule.",
        "rationale": "Use Security policy settings to create rules that exactly define the traffic to which the rules apply (zones, IP addresses, users, applications). Policies that are too general may match traffic you don’t want the policy to match and either permit undesirable traffic or deny legitimate traffic. Defining the source, destination, or both zones prevents potentially malicious traffic that uses evasive or deceptive techniques to avoid detection or appear benign from traversing the entire network, which reduces the attack surface and the threat scope. The exception to this best practice is when the Security policy needs to protect the entire network. For example, a rule that blocks traffic to malware or phishing URL categories can apply to all zones (and all traffic) because the URL Category clearly defines the traffic to block. Another example is blocking all unknown traffic with a block rule that applies to all traffic in all zones and defining the blocked applications as “unknown-tcp”, “unknown-udp”, and “unknown-p2p”.",
        "references": "['https://www.paloaltonetworks.com/documentation/81/best-practices/best-practices-internet-gateway/best-practice-internet-gateway-security-policy/define-the-initial-internet-gateway-security-policy']",
        "active": True,
        "last_updated_date": "2020-10-05T22:46:57.585179Z",
        "capability_label": [
            "Preventative",
            "Corrective"
        ],
        "class_label": [
            "Technical"
        ],
        "control_category": [
            "Access Control"
        ],
        "cscv6_control": [
            "11.1",
            "12.1"
        ],
        "cscv7_control": [
            "11.1",
            "12.3"
        ],
        "complexity": "Advanced",
        "effort": 60
    },
    {
        "doc_id": 5,
        "top_nav": "Policies",
        "left_nav": "Security",
        "title": "Service != any",
        "doc_type": "Warning",
        "description": "Configure a specific service/port for the rule.",
        "rationale": "In Security policy rules that allow traffic, never set the service port to “any”. Always specify the application and service port to prevent malware from accessing the network through open ports. The best service choice for most applications is “application-default”. When you set the service to application-default, the firewall opens only the ports defined as default ports for the specified application. The firewall also dynamically updates the rule if the default port definition for an application changes, so the firewall always opens only the default ports for the specified application’s traffic. If an application must use a non-standard port, manually define the port in the rule, and update the rule if you need to change or add ports. Only open the service ports required for each application to reduce the attack surface.",
        "references": "['https://www.paloaltonetworks.com/documentation/81/pan-os/pan-os/policy/security-policy/components-of-a-security-policy-rule']",
        "active": True,
        "last_updated_date": "2020-10-05T22:46:57.590800Z",
        "capability_label": [
            "Preventative",
            "Corrective"
        ],
        "class_label": [
            "Technical"
        ],
        "control_category": [
            "Access Control"
        ],
        "cscv6_control": [
            "9.6",
            "13.3"
        ],
        "cscv7_control": [
            "9.5",
            "13.3"
        ],
        "complexity": "Advanced",
        "effort": 60
    },
    {
        "doc_id": 6,
        "top_nav": "Policies",
        "left_nav": "Security",
        "title": "Log at Start of Session",
        "doc_type": "Warning",
        "description": "Don't enable \"Log at Session Start\" in a rule except for troubleshooting purposes.",
        "rationale": "By default, the firewall creates logs at the end of the session for all sessions that match a Security policy rule because the application identification is likely to change as the firewall identifies the specific application and because logging at the session end consumes fewer resources than logging the session start. For example, at the start of a session, the firewall identifies Facebook traffic as web-browsing traffic, but after examining a few packets, the firewall refines the application to Facebook-base. Use “Log at Session Start” only to troubleshoot packet flow and related issues, or for tunnel session logs (only logging at session start shows active GRE tunnels in the Application Command Center).",
        "references": "['https://www.paloaltonetworks.com/documentation/81/best-practices/best-practices-data-center/data-center-best-practice-security-policy/log-and-monitor-data-center-traffic/what-data-center-traffic-to-log-and-monitor']",
        "active": True,
        "last_updated_date": "2020-10-05T22:46:57.596239Z",
        "capability_label": [
            "Performance"
        ],
        "class_label": [
            "Technical"
        ],
        "control_category": [
            "Audit and Accountability"
        ],
        "cscv6_control": [],
        "cscv7_control": [],
        "complexity": "Advanced",
        "effort": 60
    },
    {
        "doc_id": 7,
        "top_nav": "Policies",
        "left_nav": "Security",
        "title": "Log Forwarding",
        "doc_type": "Warning",
        "description": "Create and enable a Log Forwarding profile on the rule.",
        "rationale": "The firewall has limited log storage space and when the space fills up, the firewall purges the oldest logs. Configure Log Forwarding for the traffic that matches each Security policy rule. You can create profiles that send logs to a dedicated storage device such as Panorama in Log Collector mode, a syslog or SNMP server, or to an email profile, to provide redundant storage for the logs on the firewall and a long-term repository for older logs. You can create profiles to forward logs to one or more external storage devices to remain in compliance, run analytics, and review abnormal activity, threat behaviors, and long-term patterns.",
        "references": "['https://www.paloaltonetworks.com/documentation/81/pan-os/pan-os/monitoring/configure-log-forwarding']",
        "active": True,
        "last_updated_date": "2020-10-05T22:46:57.601517Z",
        "capability_label": [
            "Recovery",
            "Detective"
        ],
        "class_label": [
            "Operational",
            "Technical"
        ],
        "control_category": [
            "Contingency Planning",
            "Audit and Accountability"
        ],
        "cscv6_control": [
            "6.2",
            "6.6",
            "10.1"
        ],
        "cscv7_control": [
            "6.3",
            "6.6",
            "10.1"
        ],
        "complexity": "Advanced",
        "effort": 60
    },
    {
        "doc_id": 8,
        "top_nav": "Policies",
        "left_nav": "Security",
        "title": "Expired Non-Recurring Schedules",
        "doc_type": "Warning",
        "description": "Remove or modify Security policy rules with expired non-recurring schedules.",
        "rationale": "For troubleshooting sessions, upgrade processes, or one-time events, you may configure a Security policy rule with a non-recurring schedule so that the rule takes effect only during the scheduled time period. At the end of the scheduled time period, the rule no longer affects traffic. If you want the rule to continue to be in effect, apply a different schedule to the rule or remove the schedule from the rule. If you don’t need the rule, delete the rule to prevent the rulebase from becoming cluttered.",
        "references": "['https://www.paloaltonetworks.com/documentation/81/pan-os/web-interface-help/objects/objects-schedules']",
        "active": True,
        "last_updated_date": "2020-10-05T22:46:57.606834Z",
        "capability_label": [
            "Preventative"
        ],
        "class_label": [
            "Operational"
        ],
        "control_category": [
            "Configuration Management"
        ],
        "cscv6_control": [],
        "cscv7_control": [],
        "complexity": "Easy",
        "effort": 5
    },
    {
        "doc_id": 9,
        "top_nav": "Policies",
        "left_nav": "Security",
        "title": "Disable Server Response Inspection",
        "doc_type": "Warning",
        "description": "Do not disable server response inspection on Security policy rules.",
        "rationale": "Disabling server response inspection disables packet inspection on traffic from the server to the client, which means the firewall would not inspect server-to-client flows, so it can’t protect your network against threats in those flows. Reduce the attack surface by inspecting both directions of session flows.",
        "references": "['https://www.paloaltonetworks.com/documentation/81/pan-os/pan-os/policy/security-policy/create-a-security-policy-rule']",
        "active": True,
        "last_updated_date": "2020-10-05T22:46:57.611843Z",
        "capability_label": [
            "Preventative"
        ],
        "class_label": [
            "Operational"
        ],
        "control_category": [
            "System and Information Integrity"
        ],
        "cscv6_control": [
            "8.1",
            "8.5",
            "11.1"
        ],
        "cscv7_control": [
            "8.1",
            "11.1"
        ],
        "complexity": "Advanced",
        "effort": 60
    },
    {
        "doc_id": 11,
        "top_nav": "Policies",
        "left_nav": "Security",
        "title": "Disabled Rules",
        "doc_type": "Warning",
        "description": "Remove disabled rules from the Security policy rulebase.",
        "rationale": "Delete disabled Security policy rules created for temporary purposes, testing, or that have become obsolete to keep the rulebase uncluttered.",
        "references": "['https://www.paloaltonetworks.com/documentation/81/best-practices/best-practices-internet-gateway/best-practice-internet-gateway-security-policy/remove-the-temporary-rules']",
        "active": True,
        "last_updated_date": "2020-10-05T22:46:57.616823Z",
        "capability_label": [
            "Preventative"
        ],
        "class_label": [
            "Operational"
        ],
        "control_category": [
            "Configuration Management"
        ],
        "cscv6_control": [],
        "cscv7_control": [],
        "complexity": "Easy",
        "effort": 5
    },
    {
        "doc_id": 12,
        "top_nav": "Policies",
        "left_nav": "Security",
        "title": "Interzone Deny Rule with Logging",
        "doc_type": "Warning",
        "description": "Modify (Override) the default interzone deny rule to enable logging at the session end.",
        "rationale": "The firewall has a default Security policy rule at the bottom of the rulebase (“interzone-default”) that denies all traffic between zones. You must create specific rules to allow traffic between zones. Override the rule and enable Log at Session End to gain visibility into the traffic that the interzone-default rule denies so you can evaluate whether legitimate traffic is inadvertently being denied or if recent changes deny traffic you want to allow.",
        "references": "['https://www.paloaltonetworks.com/documentation/81/best-practices/best-practices-data-center/data-center-best-practice-security-policy/log-and-monitor-data-center-traffic/log-data-center-traffic-that-matches-no-interzone-rules']",
        "active": True,
        "last_updated_date": "2020-10-05T22:46:57.622082Z",
        "capability_label": [
            "Preventative",
            "Detective"
        ],
        "class_label": [
            "Technical"
        ],
        "control_category": [
            "Audit and Accountability",
            "System and Information Integrity"
        ],
        "cscv6_control": [
            "6.2",
            "6.4",
            "6.6"
        ],
        "cscv7_control": [
            "6.2",
            "6.7",
            "6.8"
        ],
        "complexity": "Advanced",
        "effort": 60
    },
    {
        "doc_id": 13,
        "top_nav": "Policies",
        "left_nav": "Security",
        "title": "Intrazone Allow Rules with Logging",
        "doc_type": "Warning",
        "description": "Modify (Override) the default intrazone allow rule to enable logging at the session end.",
        "rationale": "The firewall has a default Security policy rule at the bottom of the rulebase (“intrazone-default”) that allows all traffic whose source and destination are within the same zone. Override the rule, enable “Log at Session End” to gain visibility into the allowed traffic, and apply at least the Antivirus, Anti-Spyware, and Vulnerability Protection Security profiles to protect against threats. It is a good practice to create a separate rule for each zone to track logs specific to each zone’s intrazone traffic (otherwise, all intrazone traffic for every zone is in one log because there’s only one rule to log). Separate rules also enable you to apply different Security profiles to different zones, if necessary. For each intrazone rule, set the zone as both the source and destination zone. Set the rest of the source and destination objects, the application, and the service to “any” to log all intrazone traffic that matches the default allow rule. Apply Security profiles to the rule and set the rule to Log at Session End. Place each zone-specific intrazone rule above the default intrazone rule in the Security policy rulebase.",
        "references": "['https://www.paloaltonetworks.com/documentation/81/best-practices/best-practices-data-center/data-center-best-practice-security-policy/log-and-monitor-data-center-traffic/log-intra-data-center-traffic-that-matches-the-intrazone-allow-rule']",
        "active": True,
        "last_updated_date": "2020-10-05T22:46:57.627846Z",
        "capability_label": [
            "Preventative",
            "Detective"
        ],
        "class_label": [
            "Technical"
        ],
        "control_category": [
            "Audit and Accountability",
            "System and Information Integrity"
        ],
        "cscv6_control": [
            "6.2",
            "6.6",
            "8.1"
        ],
        "cscv7_control": [
            "6.2",
            "6.7",
            "6.8"
        ],
        "complexity": "Advanced",
        "effort": 60
    }
]
