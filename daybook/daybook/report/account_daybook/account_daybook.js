// Copyright (c) 2025, sanket and contributors
// For license information, please see license.txt

frappe.query_reports["Account Daybook"] = {
	filters: [
        { fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            width: "80",
            options: "Company",
            reqd: 1,
            default: frappe.defaults.get_default("company"), },
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1
        },
        {
            fieldname: "doctype_filter",
            label: "Doctypes",
            fieldtype: "MultiSelect",
            options: [
              "Sales Invoice",
              "Purchase Invoice",
              "Journal Entry",
              "Purchase Receipt",
              "Delivery Note",
              "Sales Order",
              "Purchase Order",
              "Expense Claim",
            ].join("\n"),
            default: ""
          },
    ]
};
