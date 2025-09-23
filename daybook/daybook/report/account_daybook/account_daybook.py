# # # Copyright (c) 2025, sanket and contributors
# # # For license information, please see license.txt

# # import frappe





# from __future__ import unicode_literals
# import frappe
# from frappe.utils import getdate, flt, get_link_to_form

# # --- FX helper: convert any currency to INR on/before a given date ---
# def get_rate_to_inr(from_currency: str, on_date=None) -> float:
#     if not from_currency or from_currency == "INR":
#         return 1.0

#     date = getdate(on_date) if on_date else getdate()

#     try:
#         from erpnext.setup.utils import get_exchange_rate as erp_get_rate
#         r = flt(erp_get_rate(from_currency, "INR", date))
#         if r:
#             return r
#         r_rev = flt(erp_get_rate("INR", from_currency, date))
#         if r_rev:
#             return 1.0 / r_rev
#     except Exception:
#         pass

#     rate = frappe.db.get_value(
#         "Currency Exchange",
#         {"from_currency": from_currency, "to_currency": "INR", "date": ["<=", date]},
#         "exchange_rate",
#         order_by="date desc",
#     )
#     if rate:
#         return flt(rate)

#     rev = frappe.db.get_value(
#         "Currency Exchange",
#         {"from_currency": "INR", "to_currency": from_currency, "date": ["<=", date]},
#         "exchange_rate",
#         order_by="date desc",
#     )
#     if rev:
#         return 1.0 / flt(rev)

#     return 1.0


# def get_gl_entries_by_voucher(company=None):
#     gl_filters = {"docstatus": 1}
#     if company:
#         gl_filters["company"] = company

#     gl_entries = frappe.get_all(
#         "GL Entry",
#         fields=[
#             "voucher_type",
#             "voucher_no",
#             "account",
#             "debit",
#             "credit",
#             "debit_in_account_currency",
#             "credit_in_account_currency",
#             "name",
#             "company",
#             "transaction_currency",
#             "posting_date",
#             "account_currency",
#         ],
#         filters=gl_filters,
#         order_by="posting_date asc",
#     )

#     for e in gl_entries:
#         if getattr(e, "company", None):
#             e.company_currency = frappe.get_cached_value("Company", e.company, "default_currency")
#         else:
#             e.company_currency = "INR"

#     gl_map = {}
#     for entry in gl_entries:
#         key = (entry.voucher_type, entry.voucher_no)
#         gl_map.setdefault(key, []).append(entry)
#     return gl_map


# def execute(filters=None):
#     filters = filters or {}
#     company_filter = filters.get("company")

#     # parse optional doctype filter
#     doctype_filter = set()
#     if filters.get("doctype_filter"):
#         raw = filters["doctype_filter"]
#         if isinstance(raw, list):
#             doctype_filter = set([d for d in raw if d])
#         else:
#             doctype_filter = set(d.strip() for d in raw.replace("\n", ",").split(",") if d.strip())

#     gl_map = get_gl_entries_by_voucher(company_filter)

#     # Columns: include new Document Creation Date after txn_date
#     columns = [
#         {"label": "Document Type", "fieldname": "doctype", "fieldtype": "Data", "width": 150},
#         {"label": "Document / Item / Payment", "fieldname": "doc_name", "fieldtype": "Dynamic Link", "options": "doctype", "width": 300, "filterable": 1, "in_standard_filter": 1},
#         {"label": "Reference Doc", "fieldname": "reference_doc", "fieldtype": "Data", "width": 250},

#         {"label": "Company Currency", "fieldname": "company_currency", "fieldtype": "Data", "hidden": 1},
#         {"label": "Txn Currency", "fieldname": "txn_currency", "fieldtype": "Data", "hidden": 1},

#         {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "options": "txn_currency", "width": 120},

#         {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Rounded Total", "fieldname": "rounded_total", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Outstanding Amt", "fieldname": "outstanding_amount", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "options": "txn_currency", "width": 100},
#         {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "options": "txn_currency", "width": 120},

#         {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 200},
#         {"label": "GL Entry", "fieldname": "gl_entry", "fieldtype": "Data", "width": 250},
#         {"label": "Currency", "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 100},

#         {"label": "Exchange Rate", "fieldname": "exchange_rate", "fieldtype": "Float", "width": 100},

#         # These three columns will now display amounts in company default currency.
#         {"label": "Amount (Currency)", "fieldname": "amount_currency", "fieldtype": "Currency", "options": "company_currency", "width": 120},
#         {"label": "Amount (Local)", "fieldname": "amount_local", "fieldtype": "Currency", "options": "company_currency", "width": 120},
#         {"label": "Amount (Reporting)", "fieldname": "amount_reporting", "fieldtype": "Currency", "options": "INR", "width": 120},
#         {"label": "Amount (Transaction)", "fieldname": "amount_transaction", "fieldtype": "Currency", "options": "company_currency", "width": 120},

#         {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 180},
#         {"label": "Account Effect", "fieldname": "account_effect", "fieldtype": "Data", "width": 120},

#         {"label": "Transaction Date", "fieldname": "txn_date", "fieldtype": "Date", "width": 120},
#         {"label": "Document Creation Date", "fieldname": "doc_creation_date", "fieldtype": "Date", "width": 150},

#         {"label": "Bank Account", "fieldname": "bank_account_txn", "fieldtype": "Link", "options": "Bank Account", "width": 150},
#         {"label": "Allocated Amount", "fieldname": "allocated_amount", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Deposit", "fieldname": "deposit", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Withdrawal", "fieldname": "withdrawal", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Reference Number", "fieldname": "cheque_no", "fieldtype": "Data", "width": 150},
#         {"label": "Reference Date", "fieldname": "custom_document_creation_date_", "fieldtype": "Date", "width": 120},
#     ]

#     data = []
#     doc_totals = {}

#     bank_txn_meta_fields = [f.fieldname for f in frappe.get_meta("Bank Transaction").fields]
#     has_ref_fields = "reference_doctype" in bank_txn_meta_fields and "reference_name" in bank_txn_meta_fields

#     bank_txn_fields = ["date", "bank_account", "allocated_amount", "deposit", "withdrawal", "reference_number"]
#     if "reference_date" in bank_txn_meta_fields:
#         bank_txn_fields.append("reference_date")

#     doctypes = [
#         {"doctype": "Sales Invoice", "item_table": "Sales Invoice Item"},
#         {"doctype": "Purchase Invoice", "item_table": "Purchase Invoice Item"},
#         {"doctype": "Journal Entry", "item_table": "Journal Entry Account"},
#         {"doctype": "Purchase Receipt", "item_table": "Purchase Receipt Item"},
#         {"doctype": "Delivery Note", "item_table": "Delivery Note Item"},
#         {"doctype": "Sales Order", "item_table": "Sales Order Item"},
#         {"doctype": "Purchase Order", "item_table": "Purchase Order Item"},
#         {"doctype": "Expense Claim", "item_table": "Expense Claim Detail"},
#     ]

#     for dt in doctypes:
#         doctype = dt["doctype"]
#         item_table = dt.get("item_table")

#         if doctype_filter and doctype not in doctype_filter:
#             continue

#         try:
#             meta = frappe.get_meta(doctype)
#         except frappe.DoesNotExistError:
#             continue

#         available_fields = [df.fieldname for df in meta.fields]
#         fields = ["name"]

#         # include company and monetary fields when present
#         if "company" in available_fields:
#             fields.append("company")
#         if "grand_total" in available_fields:
#             fields.append("grand_total")
#         if "rounded_total" in available_fields:
#             fields.append("rounded_total")
#         if "outstanding_amount" in available_fields:
#             fields.append("outstanding_amount")
#         if "currency" in available_fields:
#             fields.append("currency")
#         if "conversion_rate" in available_fields:
#             fields.append("conversion_rate")

#         # include custom_document_creation_date_ if available (needed for Document Creation Date for Journal Entry)
#         if "custom_document_creation_date_" in available_fields:
#             fields.append("custom_document_creation_date_")

#         # include a suitable date field and remember which one
#         date_field = None
#         if "posting_date" in available_fields:
#             date_field = "posting_date"
#         elif "transaction_date" in available_fields:
#             date_field = "transaction_date"
#         if date_field and date_field not in fields:
#             fields.append(date_field)

#         if doctype == "Journal Entry":
#             fields += ["total_debit", "total_credit"]
#             # Journal Entry may have custom_document_creation_date_ already added above
#         if doctype in ["Sales Order", "Purchase Order"]:
#             if "transaction_date" not in fields and "transaction_date" in available_fields:
#                 fields.append("transaction_date")
#             if "currency" not in fields and "currency" in available_fields:
#                 fields.append("currency")
#             if "conversion_rate" not in fields and "conversion_rate" in available_fields:
#                 fields.append("conversion_rate")
#         if doctype == "Sales Order":
#             if "selling_price_list" in available_fields:
#                 fields.append("selling_price_list")

#         doc_totals[doctype] = 0.0

#         # filters
#         filters_dict = {"docstatus": 1}
#         if "company" in available_fields and company_filter:
#             filters_dict["company"] = company_filter
#         if date_field and filters and filters.get("from_date") and filters.get("to_date"):
#             filters_dict[date_field] = ["between", [filters["from_date"], filters["to_date"]]]

#         records = frappe.get_all(doctype, filters=filters_dict, fields=fields, ignore_permissions=True)

#         for rec in records:
#             name = rec.get("name")
#             grand_total = rec.get("grand_total")
#             rounded_total = rec.get("rounded_total")
#             outstanding = rec.get("outstanding_amount")
#             total_debit = rec.get("total_debit")
#             total_credit = rec.get("total_credit")
#             currency = rec.get("currency")
#             if not currency:
#                 default_company = rec.get("company") or frappe.db.get_default("company")
#                 currency = frappe.get_cached_value("Company", default_company, "default_currency") if default_company else "INR"

#             selling_price_list = rec.get("selling_price_list") if doctype == "Sales Order" else None

#             # Decide document date for FX
#             doc_date = rec.get(date_field) if date_field else None
#             txn_date = rec.get("transaction_date") if "transaction_date" in rec else (rec.get("posting_date") if "posting_date" in rec else None)

#             # Base amounts in document currency
#             if doctype == "Journal Entry":
#                 amount_currency_doc = grand_total or total_debit or 0.0
#             else:
#                 amount_currency_doc = grand_total or 0.0

#             # Determine exchange_rate from document if available (use conversion_rate when present)
#             if "conversion_rate" in available_fields:
#                 conversion_rate = rec.get("conversion_rate") or 1
#             else:
#                 conversion_rate = 1

#             # Reporting (INR) conversion (use document date)
#             rate_to_inr = get_rate_to_inr(currency, doc_date)
#             amount_reporting = amount_currency_doc * rate_to_inr  # ALWAYS INR

#             # amount_local (company currency) using conversion_rate when available
#             # company default currency:
#             company_name = rec.get("company") if "company" in rec else frappe.db.get_default("company")
#             company_currency = frappe.get_cached_value("Company", company_name, "default_currency") if company_name else "INR"

#             # Convert document amounts to company currency for display columns:
#             if currency and company_currency and currency != company_currency:
#                 # Prefer conversion_rate from document if present (document currency -> company currency)
#                 # conversion_rate means: 1 doc_currency = conversion_rate company_currency
#                 amount_in_company = amount_currency_doc * (conversion_rate or 1)
#             else:
#                 amount_in_company = amount_currency_doc

#             amount_local = amount_in_company
#             amount_transaction = amount_in_company
#             amount_currency = amount_in_company  # display in company currency as requested

#             if grand_total:
#                 doc_totals[doctype] += grand_total
#             elif total_debit:
#                 doc_totals[doctype] += total_debit

#             # Build reference_doc from child tables where applicable
#             reference_doc = None
#             if doctype in ["Sales Invoice", "Purchase Invoice", "Purchase Receipt", "Delivery Note"]:
#                 child_table = {
#                     "Sales Invoice": ("Sales Invoice Item", "sales_order"),
#                     "Purchase Invoice": ("Purchase Invoice Item", "purchase_order"),
#                     "Purchase Receipt": ("Purchase Receipt Item", "sales_order"),
#                     "Delivery Note": ("Delivery Note Item", "against_sales_order"),
#                 }
#                 item_table, reference_field = child_table[doctype]
#                 references = frappe.get_all(item_table, filters={"parent": name}, fields=[reference_field])
#                 ref_set = set([r[reference_field] for r in references if r.get(reference_field)])
#                 reference_doc = ", ".join(ref_set) if ref_set else None

#             account_effect_flag = "Yes" if gl_map.get((doctype, name)) else "No"

#             # Populate doc_creation_date only for Journal Entry (use custom_document_creation_date_ if present)
#             doc_creation_date_val = None
#             if doctype == "Journal Entry":
#                 # prefer custom_document_creation_date_ if present in the record
#                 doc_creation_date_val = rec.get("custom_document_creation_date_") if rec.get("custom_document_creation_date_") else None

#             base_row = {
#                 "doctype": doctype,          # used by Dynamic Link column
#                 "doc_name": name,           # actual doc name (clickable)
#                 "reference_doc": reference_doc,

#                 "grand_total": grand_total,
#                 "rounded_total": rounded_total,
#                 "outstanding_amount": outstanding,

#                 "rate": conversion_rate if conversion_rate else None,
#                 # these amount columns are now shown in company default currency
#                 "amount_currency": amount_currency,
#                 "amount_local": amount_local,
#                 "amount_reporting": amount_reporting,
#                 "amount_transaction": amount_transaction,

#                 "amount": None,
#                 "account": None,
#                 "debit": None,
#                 "credit": None,
#                 "total_debit": total_debit,
#                 "total_credit": total_credit,
#                 "gl_entry": None,
#                 "txn_date": txn_date,

#                 # New field: Document Creation Date (custom_document_creation_date_ for Journal Entry)
#                 "doc_creation_date": doc_creation_date_val,

#                 "bank_account_txn": None,
#                 "allocated_amount": None,
#                 "deposit": None,
#                 "withdrawal": None,
#                 "cheque_no": None,
#                 "custom_document_creation_date_": None,

#                 # currency helpers
#                 "currency": currency,               # visible column (doc currency)
#                 "txn_currency": currency,           # used by txn columns
#                 "company_currency": company_currency,  # used by company columns (column 'options' refer to this)
#                 "selling_price_list": selling_price_list,
#                 "exchange_rate": conversion_rate,
#                 "company": company_name,
#                 "account_effect": account_effect_flag,
#                 "indent": 0,
#             }
#             data.append(base_row)

#             # --- GL Entry detail lines ---
#             for gle in gl_map.get((doctype, name), []):
#                 signed_amount = (gle.debit or 0.0) - (gle.credit or 0.0)  # signed amount in company currency

#                 row_currency = getattr(gle, "account_currency", None) or getattr(gle, "transaction_currency", None)
#                 gl_company = gle.company if getattr(gle, "company", None) else company_name
#                 company_currency_gl = frappe.get_cached_value("Company", gl_company, "default_currency") if gl_company else "INR"

#                 if row_currency and row_currency != company_currency_gl and (
#                     getattr(gle, "debit_in_account_currency", None) is not None
#                     or getattr(gle, "credit_in_account_currency", None) is not None
#                 ):
#                     amount_currency_gl = (gle.debit_in_account_currency or 0.0) - (gle.credit_in_account_currency or 0.0)
#                     if amount_currency_gl:
#                         exchange_rate_row_to_company = abs(signed_amount) / abs(amount_currency_gl)
#                     else:
#                         exchange_rate_row_to_company = 1.0
#                 else:
#                     exchange_rate_row_to_company = 1.0
#                     amount_currency_gl = signed_amount
#                     if doctype == "Journal Entry" and row_currency and row_currency != company_currency_gl:
#                         jea_rate = frappe.db.get_value(
#                             "Journal Entry Account",
#                             {"parent": gle.voucher_no, "account": gle.account},
#                             "exchange_rate",
#                         ) or 0
#                         if jea_rate:
#                             exchange_rate_row_to_company = jea_rate
#                             amount_currency_gl = signed_amount / jea_rate

#                 rate_company_to_inr = get_rate_to_inr(company_currency_gl, getattr(gle, "posting_date", None) or doc_date)
#                 amount_reporting_gl = signed_amount * rate_company_to_inr

#                 if row_currency and row_currency != company_currency_gl:
#                     debit_val = gle.debit_in_account_currency or 0.0
#                     credit_val = gle.credit_in_account_currency or 0.0
#                     amount_local_gl = debit_val - credit_val
#                     display_currency = row_currency
#                 else:
#                     debit_val = gle.debit or 0.0
#                     credit_val = gle.credit or 0.0
#                     amount_local_gl = debit_val - credit_val
#                     display_currency = company_currency_gl

#                 # For GL child rows, signed_amount is already in company currency — show that for the 3 columns
#                 data.append({
#                     "doctype": "GL Entry",
#                     "doc_name": gle.name,
#                     "reference_doc": name,

#                     "account": gle.account,
#                     "debit": debit_val,
#                     "credit": credit_val,
#                     # Display amounts in company currency (signed_amount)
#                     "amount_currency": signed_amount,
#                     "amount_local": signed_amount,
#                     "amount_reporting": amount_reporting_gl,
#                     "amount_transaction": signed_amount,

#                     "gl_entry": get_link_to_form("GL Entry", gle.name),

#                     "company": gl_company,
#                     "account_effect": "Yes",

#                     # currency helpers
#                     "currency": display_currency,
#                     "txn_currency": display_currency,
#                     "company_currency": company_currency_gl,
#                     "exchange_rate": exchange_rate_row_to_company,

#                     # show GL posting date in txn_date
#                     "txn_date": gle.posting_date,
#                     # GL / child rows do not show doc_creation_date
#                     "doc_creation_date": None,

#                     "indent": 1,
#                 })

#             # --- Payment Entries linked to this document ---
#             payment_refs = frappe.get_all(
#                 "Payment Entry Reference",
#                 fields=["parent"],
#                 filters={"reference_doctype": doctype, "reference_name": name, "docstatus": 1},
#             )

#             for pref in payment_refs:
#                 payment_entry = frappe.get_doc("Payment Entry", pref.parent)
#                 if company_filter and payment_entry.company != company_filter:
#                     continue
#                 if doctype_filter and doctype not in doctype_filter:
#                     continue

#                 payment_currency = None
#                 if getattr(payment_entry, "paid_from_account_currency", None):
#                     payment_currency = payment_entry.paid_from_account_currency
#                 elif getattr(payment_entry, "paid_to_account_currency", None):
#                     payment_currency = payment_entry.paid_to_account_currency
#                 elif getattr(payment_entry, "paid_from", None):
#                     try:
#                         payment_currency = frappe.get_cached_value("Account", payment_entry.paid_from, "account_currency")
#                     except Exception:
#                         payment_currency = None

#                 if not payment_currency:
#                     payment_currency = frappe.get_cached_value("Company", payment_entry.company, "default_currency")

#                 company_currency_pe = frappe.get_cached_value("Company", payment_entry.company, "default_currency")
#                 rate_to_inr_pe = get_rate_to_inr(payment_currency, payment_entry.posting_date)

#                 amount_currency_pe = payment_entry.paid_amount or 0.0
#                 local_rate = getattr(payment_entry, "source_exchange_rate", 1.0) or 1.0
#                 amount_local_pe = amount_currency_pe * local_rate
#                 amount_reporting_pe = amount_currency_pe * rate_to_inr_pe

#                 # Show payment amounts in company currency columns (use amount_local_pe)
#                 data.append({
#                     "doctype": "Payment Entry",
#                     "doc_name": payment_entry.name,
#                     "reference_doc": name,

#                     "grand_total": payment_entry.paid_amount,
#                     "account": payment_entry.paid_from if getattr(payment_entry, "payment_type", None) == "Receive" else payment_entry.paid_to,

#                     "amount_currency": amount_local_pe,
#                     "amount_local": amount_local_pe,
#                     "amount_reporting": amount_reporting_pe,
#                     "amount_transaction": amount_local_pe,

#                     "txn_date": payment_entry.posting_date,
#                     # Payment child rows do not show doc_creation_date
#                     "doc_creation_date": None,

#                     "cheque_no": payment_entry.reference_no,
#                     "custom_document_creation_date_": payment_entry.reference_date,
#                     "company": payment_entry.company,
#                     "account_effect": "Yes",

#                     # currency helpers
#                     "currency": payment_currency,
#                     "txn_currency": payment_currency,
#                     "company_currency": company_currency_pe,
#                     "exchange_rate": local_rate,

#                     "indent": 1,
#                 })

#     chart = {
#         "data": {
#             "labels": list(doc_totals.keys()),
#             "datasets": [{"values": list(doc_totals.values())}],
#         },
#         "type": "pie",
#         "height": 300,
#     }

#     cumulative_total = sum(doc_totals.values())
#     report_summary = [{
#         "value": cumulative_total,
#         "indicator": "Green" if cumulative_total >= 0 else "Red",
#         "label": "Cumulative Total",
#         "datatype": "Currency",
#         "currency": frappe.get_cached_value('Company', frappe.db.get_default('company'), 'default_currency')
#             if frappe.db.get_default('company') else ""
#     }]

#     return columns, data, None, chart, report_summary



# ++++++++++++++++++++++++++++++++++++++++++++++++




# Copyright (c) 2025, sanket and contributors
# For license information, please see license.txt

# import frappe




# from __future__ import unicode_literals
# import frappe
# from frappe.utils import getdate, flt, get_link_to_form

# # --- FX helper: convert any currency to INR on/before a given date ---
# def get_rate_to_inr(from_currency: str, on_date=None) -> float:
#     if not from_currency or from_currency == "INR":
#         return 1.0

#     date = getdate(on_date) if on_date else getdate()

#     try:
#         from erpnext.setup.utils import get_exchange_rate as erp_get_rate
#         r = flt(erp_get_rate(from_currency, "INR", date))
#         if r:
#             return r
#         r_rev = flt(erp_get_rate("INR", from_currency, date))
#         if r_rev:
#             return 1.0 / r_rev
#     except Exception:
#         pass

#     rate = frappe.db.get_value(
#         "Currency Exchange",
#         {"from_currency": from_currency, "to_currency": "INR", "date": ["<=", date]},
#         "exchange_rate",
#         order_by="date desc",
#     )
#     if rate:
#         return flt(rate)

#     rev = frappe.db.get_value(
#         "Currency Exchange",
#         {"from_currency": "INR", "to_currency": from_currency, "date": ["<=", date]},
#         "exchange_rate",
#         order_by="date desc",
#     )
#     if rev:
#         return 1.0 / flt(rev)

#     return 1.0


# def get_gl_entries_by_voucher(company=None):
#     gl_filters = {"docstatus": 1}
#     if company:
#         gl_filters["company"] = company

#     gl_entries = frappe.get_all(
#         "GL Entry",
#         fields=[
#             "voucher_type",
#             "voucher_no",
#             "account",
#             "debit",
#             "credit",
#             "debit_in_account_currency",
#             "credit_in_account_currency",
#             "name",
#             "company",
#             "transaction_currency",
#             "posting_date",
#             "account_currency",
#         ],
#         filters=gl_filters,
#         order_by="posting_date asc",
#     )

#     for e in gl_entries:
#         if getattr(e, "company", None):
#             e.company_currency = frappe.get_cached_value("Company", e.company, "default_currency")
#         else:
#             e.company_currency = "INR"

#     gl_map = {}
#     for entry in gl_entries:
#         key = (entry.voucher_type, entry.voucher_no)
#         gl_map.setdefault(key, []).append(entry)
#     return gl_map


# def execute(filters=None):
#     filters = filters or {}
#     company_filter = filters.get("company")

#     # parse optional doctype filter
#     doctype_filter = set()
#     if filters.get("doctype_filter"):
#         raw = filters["doctype_filter"]
#         if isinstance(raw, list):
#             doctype_filter = set([d for d in raw if d])
#         else:
#             doctype_filter = set(d.strip() for d in raw.replace("\n", ",").split(",") if d.strip())

#     gl_map = get_gl_entries_by_voucher(company_filter)

#     # Columns: include new Document Creation Date after txn_date
#     columns = [
#         {"label": "Document Type", "fieldname": "doctype", "fieldtype": "Data", "width": 150},
#         {"label": "Document / Item / Payment", "fieldname": "doc_name", "fieldtype": "Dynamic Link", "options": "doctype", "width": 300, "filterable": 1, "in_standard_filter": 1},
#         {"label": "Reference Doc", "fieldname": "reference_doc", "fieldtype": "Data", "width": 250},

#         {"label": "Company Currency", "fieldname": "company_currency", "fieldtype": "Data", "hidden": 1},
#         {"label": "Txn Currency", "fieldname": "txn_currency", "fieldtype": "Data", "hidden": 1},

#         {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "options": "txn_currency", "width": 120},

#         {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Rounded Total", "fieldname": "rounded_total", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Outstanding Amt", "fieldname": "outstanding_amount", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "options": "txn_currency", "width": 100},
#         {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "options": "txn_currency", "width": 120},

#         {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 200},
#         {"label": "GL Entry", "fieldname": "gl_entry", "fieldtype": "Data", "width": 250},
#         {"label": "Currency", "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 100},

#         {"label": "Exchange Rate", "fieldname": "exchange_rate", "fieldtype": "Float", "width": 100},

#         # These three columns will now display amounts in company default currency.
#         # {"label": "Amount (Currency)", "fieldname": "amount_currency", "fieldtype": "Currency", "options": "company_currency", "width": 120},
#         {"label": "Amount (Local)", "fieldname": "amount_local", "fieldtype": "Currency", "options": "company_currency", "width": 120},
#         {"label": "Amount (Reporting)", "fieldname": "amount_reporting", "fieldtype": "Currency", "options": "INR", "width": 120},
#         {"label": "Amount (Transaction)", "fieldname": "amount_transaction", "fieldtype": "Currency", "options": "company_currency", "width": 120},

#         {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 180},
#         {"label": "Account Effect", "fieldname": "account_effect", "fieldtype": "Data", "width": 120},

#         {"label": "Transaction Date", "fieldname": "txn_date", "fieldtype": "Date", "width": 120},
#         {"label": "Document Creation Date", "fieldname": "doc_creation_date", "fieldtype": "Date", "width": 150},

#         {"label": "Bank Account", "fieldname": "bank_account_txn", "fieldtype": "Link", "options": "Bank Account", "width": 150},
#         {"label": "Allocated Amount", "fieldname": "allocated_amount", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Deposit", "fieldname": "deposit", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Withdrawal", "fieldname": "withdrawal", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Reference Number", "fieldname": "cheque_no", "fieldtype": "Data", "width": 150},
#         {"label": "Reference Date", "fieldname": "custom_document_creation_date_", "fieldtype": "Date", "width": 120},
#     ]

#     data = []
#     doc_totals = {}

#     bank_txn_meta_fields = [f.fieldname for f in frappe.get_meta("Bank Transaction").fields]
#     has_ref_fields = "reference_doctype" in bank_txn_meta_fields and "reference_name" in bank_txn_meta_fields

#     bank_txn_fields = ["date", "bank_account", "allocated_amount", "deposit", "withdrawal", "reference_number"]
#     if "reference_date" in bank_txn_meta_fields:
#         bank_txn_fields.append("reference_date")

#     doctypes = [
#         {"doctype": "Sales Invoice", "item_table": "Sales Invoice Item"},
#         {"doctype": "Purchase Invoice", "item_table": "Purchase Invoice Item"},
#         {"doctype": "Journal Entry", "item_table": "Journal Entry Account"},
#         {"doctype": "Purchase Receipt", "item_table": "Purchase Receipt Item"},
#         {"doctype": "Delivery Note", "item_table": "Delivery Note Item"},
#         {"doctype": "Sales Order", "item_table": "Sales Order Item"},
#         {"doctype": "Purchase Order", "item_table": "Purchase Order Item"},
#         {"doctype": "Expense Claim", "item_table": "Expense Claim Detail"},
#     ]

#     for dt in doctypes:
#         doctype = dt["doctype"]
#         item_table = dt.get("item_table")

#         if doctype_filter and doctype not in doctype_filter:
#             continue

#         try:
#             meta = frappe.get_meta(doctype)
#         except frappe.DoesNotExistError:
#             continue

#         available_fields = [df.fieldname for df in meta.fields]
#         fields = ["name"]

#         # include company and monetary fields when present
#         if "company" in available_fields:
#             fields.append("company")
#         if "grand_total" in available_fields:
#             fields.append("grand_total")
#         if "rounded_total" in available_fields:
#             fields.append("rounded_total")
#         if "outstanding_amount" in available_fields:
#             fields.append("outstanding_amount")
#         if "currency" in available_fields:
#             fields.append("currency")
#         if "conversion_rate" in available_fields:
#             fields.append("conversion_rate")

#         # include custom_document_creation_date_ if available (needed for Document Creation Date for Journal Entry)
#         if "custom_document_creation_date_" in available_fields:
#             fields.append("custom_document_creation_date_")

#         # include a suitable date field and remember which one
#         date_field = None
#         if "posting_date" in available_fields:
#             date_field = "posting_date"
#         elif "transaction_date" in available_fields:
#             date_field = "transaction_date"
#         if date_field and date_field not in fields:
#             fields.append(date_field)

#         if doctype == "Journal Entry":
#             fields += ["total_debit", "total_credit"]
#             # Journal Entry may have custom_document_creation_date_ already added above
#         if doctype in ["Sales Order", "Purchase Order"]:
#             if "transaction_date" not in fields and "transaction_date" in available_fields:
#                 fields.append("transaction_date")
#             if "currency" not in fields and "currency" in available_fields:
#                 fields.append("currency")
#             if "conversion_rate" not in fields and "conversion_rate" in available_fields:
#                 fields.append("conversion_rate")
#         if doctype == "Sales Order":
#             if "selling_price_list" in available_fields:
#                 fields.append("selling_price_list")

#         doc_totals[doctype] = 0.0

#         # filters
#         filters_dict = {"docstatus": 1}
#         if "company" in available_fields and company_filter:
#             filters_dict["company"] = company_filter
#         if date_field and filters and filters.get("from_date") and filters.get("to_date"):
#             filters_dict[date_field] = ["between", [filters["from_date"], filters["to_date"]]]

#         records = frappe.get_all(doctype, filters=filters_dict, fields=fields, ignore_permissions=True)

#         for rec in records:
#             name = rec.get("name")
#             grand_total = rec.get("grand_total")
#             rounded_total = rec.get("rounded_total")
#             outstanding = rec.get("outstanding_amount")
#             total_debit = rec.get("total_debit")
#             total_credit = rec.get("total_credit")
#             currency = rec.get("currency")
#             if not currency:
#                 default_company = rec.get("company") or frappe.db.get_default("company")
#                 currency = frappe.get_cached_value("Company", default_company, "default_currency") if default_company else "INR"

#             selling_price_list = rec.get("selling_price_list") if doctype == "Sales Order" else None

#             # Decide document date for FX
#             doc_date = rec.get(date_field) if date_field else None
#             txn_date = rec.get("transaction_date") if "transaction_date" in rec else (rec.get("posting_date") if "posting_date" in rec else None)

#             # Base amounts in document currency
#             if doctype == "Journal Entry":
#                 amount_currency_doc = grand_total or total_debit or 0.0
#             else:
#                 amount_currency_doc = grand_total or 0.0

#             # Determine exchange_rate from document if available (use conversion_rate when present)
#             if "conversion_rate" in available_fields:
#                 conversion_rate = rec.get("conversion_rate") or 1
#             else:
#                 conversion_rate = 1

#             # Reporting (INR) conversion (use document date)
#             rate_to_inr = get_rate_to_inr(currency, doc_date)
#             amount_reporting = amount_currency_doc * rate_to_inr  # ALWAYS INR

#             # amount_local (company currency) using conversion_rate when available
#             # company default currency:
#             company_name = rec.get("company") if "company" in rec else frappe.db.get_default("company")
#             company_currency = frappe.get_cached_value("Company", company_name, "default_currency") if company_name else "INR"

#             # Convert document amounts to company currency for display columns:
#             if currency and company_currency and currency != company_currency:
#                 # Prefer conversion_rate from document if present (document currency -> company currency)
#                 # conversion_rate means: 1 doc_currency = conversion_rate company_currency
#                 amount_in_company = amount_currency_doc * (conversion_rate or 1)
#             else:
#                 amount_in_company = amount_currency_doc

#             amount_local = amount_in_company
#             amount_transaction = amount_in_company
#             amount_currency = amount_in_company  # display in company currency as requested

#             if grand_total:
#                 doc_totals[doctype] += grand_total
#             elif total_debit:
#                 doc_totals[doctype] += total_debit

#             # Build reference_doc from child tables where applicable
#             reference_doc = None
#             if doctype in ["Sales Invoice", "Purchase Invoice", "Purchase Receipt", "Delivery Note"]:
#                 child_table = {
#                     "Sales Invoice": ("Sales Invoice Item", "sales_order"),
#                     "Purchase Invoice": ("Purchase Invoice Item", "purchase_order"),
#                     "Purchase Receipt": ("Purchase Receipt Item", "sales_order"),
#                     "Delivery Note": ("Delivery Note Item", "against_sales_order"),
#                 }
#                 item_table, reference_field = child_table[doctype]
#                 references = frappe.get_all(item_table, filters={"parent": name}, fields=[reference_field])
#                 ref_set = set([r[reference_field] for r in references if r.get(reference_field)])
#                 reference_doc = ", ".join(ref_set) if ref_set else None

#             account_effect_flag = "Yes" if gl_map.get((doctype, name)) else "No"

#             # Populate doc_creation_date only for Journal Entry (use custom_document_creation_date_ if present)
#             doc_creation_date_val = None
#             if doctype == "Journal Entry":
#                 # prefer custom_document_creation_date_ if present in the record
#                 doc_creation_date_val = rec.get("custom_document_creation_date_") if rec.get("custom_document_creation_date_") else None

#             base_row = {
#                 "doctype": doctype,          # used by Dynamic Link column
#                 "doc_name": name,           # actual doc name (clickable)
#                 "reference_doc": reference_doc,

#                 "grand_total": grand_total,
#                 "rounded_total": rounded_total,
#                 "outstanding_amount": outstanding,

#                 "rate": conversion_rate if conversion_rate else None,
#                 # these amount columns are now shown in company default currency
#                 # "amount_currency": amount_currency,
#                 "amount_local": amount_local,
#                 "amount_reporting": amount_reporting,
#                 "amount_transaction": amount_transaction,

#                 "amount": None,
#                 "account": None,
#                 "debit": None,
#                 "credit": None,
#                 "total_debit": total_debit,
#                 "total_credit": total_credit,
#                 "gl_entry": None,
#                 "txn_date": txn_date,

#                 # New field: Document Creation Date (custom_document_creation_date_ for Journal Entry)
#                 "doc_creation_date": doc_creation_date_val,

#                 "bank_account_txn": None,
#                 "allocated_amount": None,
#                 "deposit": None,
#                 "withdrawal": None,
#                 "cheque_no": None,
#                 "custom_document_creation_date_": None,

#                 # currency helpers
#                 "currency": currency,               # visible column (doc currency)
#                 "txn_currency": currency,           # used by txn columns
#                 "company_currency": company_currency,  # used by company columns (column 'options' refer to this)
#                 "selling_price_list": selling_price_list,
#                 "exchange_rate": conversion_rate,
#                 "company": company_name,
#                 # "account_effect": account_effect_flag,
#                 "account_effect": "Main",
#                 "indent": 0,
#             }
#             data.append(base_row)

#             # --- GL Entry detail lines ---
#             for gle in gl_map.get((doctype, name), []):
#                 signed_amount = (gle.debit or 0.0) - (gle.credit or 0.0)  # signed amount in company currency

#                 row_currency = getattr(gle, "account_currency", None) or getattr(gle, "transaction_currency", None)
#                 gl_company = gle.company if getattr(gle, "company", None) else company_name
#                 company_currency_gl = frappe.get_cached_value("Company", gl_company, "default_currency") if gl_company else "INR"

#                 if row_currency and row_currency != company_currency_gl and (
#                     getattr(gle, "debit_in_account_currency", None) is not None
#                     or getattr(gle, "credit_in_account_currency", None) is not None
#                 ):
#                     amount_currency_gl = (gle.debit_in_account_currency or 0.0) - (gle.credit_in_account_currency or 0.0)
#                     if amount_currency_gl:
#                         exchange_rate_row_to_company = abs(signed_amount) / abs(amount_currency_gl)
#                     else:
#                         exchange_rate_row_to_company = 1.0
#                 else:
#                     exchange_rate_row_to_company = 1.0
#                     amount_currency_gl = signed_amount
#                     if doctype == "Journal Entry" and row_currency and row_currency != company_currency_gl:
#                         jea_rate = frappe.db.get_value(
#                             "Journal Entry Account",
#                             {"parent": gle.voucher_no, "account": gle.account},
#                             "exchange_rate",
#                         ) or 0
#                         if jea_rate:
#                             exchange_rate_row_to_company = jea_rate
#                             amount_currency_gl = signed_amount / jea_rate

#                 rate_company_to_inr = get_rate_to_inr(company_currency_gl, getattr(gle, "posting_date", None) or doc_date)
#                 amount_reporting_gl = signed_amount * rate_company_to_inr

#                 if row_currency and row_currency != company_currency_gl:
#                     debit_val = gle.debit_in_account_currency or 0.0
#                     credit_val = gle.credit_in_account_currency or 0.0
#                     amount_local_gl = debit_val - credit_val
#                     display_currency = row_currency
#                 else:
#                     debit_val = gle.debit or 0.0
#                     credit_val = gle.credit or 0.0
#                     amount_local_gl = debit_val - credit_val
#                     display_currency = company_currency_gl

#                 # For GL child rows, signed_amount is already in company currency — show that for the 3 columns
#                 data.append({
#                     "doctype": "GL Entry",
#                     "doc_name": gle.name,
#                     "reference_doc": name,

#                     "account": gle.account,
#                     "debit": debit_val,
#                     "credit": credit_val,
#                     # Display amounts in company currency (signed_amount)
#                     # "amount_currency": signed_amount,
#                     "amount_local": signed_amount,
#                     "amount_reporting": amount_reporting_gl,
#                     "amount_transaction": signed_amount,

#                     "gl_entry": get_link_to_form("GL Entry", gle.name),

#                     "company": gl_company,
#                     "account_effect": "Yes",

#                     # currency helpers
#                     "currency": display_currency,
#                     "txn_currency": display_currency,
#                     "company_currency": company_currency_gl,
#                     "exchange_rate": exchange_rate_row_to_company,

#                     # show GL posting date in txn_date
#                     "txn_date": gle.posting_date,
#                     # GL / child rows do not show doc_creation_date
#                     "doc_creation_date": None,

#                     "indent": 1,
#                 })

#             # --- Payment Entries linked to this document ---
#             payment_refs = frappe.get_all(
#                 "Payment Entry Reference",
#                 fields=["parent"],
#                 filters={"reference_doctype": doctype, "reference_name": name, "docstatus": 1},
#             )

#             for pref in payment_refs:
#                 payment_entry = frappe.get_doc("Payment Entry", pref.parent)
#                 if company_filter and payment_entry.company != company_filter:
#                     continue
#                 if doctype_filter and doctype not in doctype_filter:
#                     continue

#                 payment_currency = None
#                 if getattr(payment_entry, "paid_from_account_currency", None):
#                     payment_currency = payment_entry.paid_from_account_currency
#                 elif getattr(payment_entry, "paid_to_account_currency", None):
#                     payment_currency = payment_entry.paid_to_account_currency
#                 elif getattr(payment_entry, "paid_from", None):
#                     try:
#                         payment_currency = frappe.get_cached_value("Account", payment_entry.paid_from, "account_currency")
#                     except Exception:
#                         payment_currency = None

#                 if not payment_currency:
#                     payment_currency = frappe.get_cached_value("Company", payment_entry.company, "default_currency")

#                 company_currency_pe = frappe.get_cached_value("Company", payment_entry.company, "default_currency")
#                 rate_to_inr_pe = get_rate_to_inr(payment_currency, payment_entry.posting_date)

#                 amount_currency_pe = payment_entry.paid_amount or 0.0
#                 local_rate = getattr(payment_entry, "source_exchange_rate", 1.0) or 1.0
#                 amount_local_pe = amount_currency_pe * local_rate
#                 amount_reporting_pe = amount_currency_pe * rate_to_inr_pe

#                 # Show payment amounts in company currency columns (use amount_local_pe)
#                 data.append({
#                     "doctype": "Payment Entry",
#                     "doc_name": payment_entry.name,
#                     "reference_doc": name,

#                     "grand_total": payment_entry.paid_amount,
#                     "account": payment_entry.paid_from if getattr(payment_entry, "payment_type", None) == "Receive" else payment_entry.paid_to,

#                     # "amount_currency": amount_local_pe,
#                     "amount_local": amount_local_pe,
#                     "amount_reporting": amount_reporting_pe,
#                     "amount_transaction": amount_local_pe,

#                     "txn_date": payment_entry.posting_date,
#                     # Payment child rows do not show doc_creation_date
#                     "doc_creation_date": None,

#                     "cheque_no": payment_entry.reference_no,
#                     "custom_document_creation_date_": payment_entry.reference_date,
#                     "company": payment_entry.company,
#                     "account_effect": "Yes",

#                     # currency helpers
#                     "currency": payment_currency,
#                     "txn_currency": payment_currency,
#                     "company_currency": company_currency_pe,
#                     "exchange_rate": local_rate,

#                     "indent": 1,
#                 })

#     chart = {
#         "data": {
#             "labels": list(doc_totals.keys()),
#             "datasets": [{"values": list(doc_totals.values())}],
#         },
#         "type": "pie",
#         "height": 300,
#     }

#     cumulative_total = sum(doc_totals.values())
#     report_summary = [{
#         "value": cumulative_total,
#         "indicator": "Green" if cumulative_total >= 0 else "Red",
#         "label": "Cumulative Total",
#         "datatype": "Currency",
#         "currency": frappe.get_cached_value('Company', frappe.db.get_default('company'), 'default_currency')
#             if frappe.db.get_default('company') else ""
#     }]

#     return columns, data, None, chart, report_summary





# ////////////////////////////////////////////////////////






# from __future__ import unicode_literals
# import frappe
# from frappe.utils import getdate, flt, get_link_to_form


# # --- FX helper: convert any currency to INR on/before a given date ---
# def get_rate_to_inr(from_currency: str, on_date=None) -> float:
#     if not from_currency or from_currency == "INR":
#         return 1.0

#     date = getdate(on_date) if on_date else getdate()

#     try:
#         from erpnext.setup.utils import get_exchange_rate as erp_get_rate
#         r = flt(erp_get_rate(from_currency, "INR", date))
#         if r:
#             return r
#         r_rev = flt(erp_get_rate("INR", from_currency, date))
#         if r_rev:
#             return 1.0 / r_rev
#     except Exception:
#         pass

#     rate = frappe.db.get_value(
#         "Currency Exchange",
#         {"from_currency": from_currency, "to_currency": "INR", "date": ["<=", date]},
#         "exchange_rate",
#         order_by="date desc",
#     )
#     if rate:
#         return flt(rate)

#     rev = frappe.db.get_value(
#         "Currency Exchange",
#         {"from_currency": "INR", "to_currency": from_currency, "date": ["<=", date]},
#         "exchange_rate",
#         order_by="date desc",
#     )
#     if rev:
#         return 1.0 / flt(rev)

#     return 1.0


# def get_gl_entries_by_voucher(company=None):
#     gl_filters = {"docstatus": 1}
#     if company:
#         gl_filters["company"] = company

#     gl_entries = frappe.get_all(
#         "GL Entry",
#         fields=[
#             "voucher_type",
#             "voucher_no",
#             "account",
#             "debit",
#             "credit",
#             "debit_in_account_currency",
#             "credit_in_account_currency",
#             "name",
#             "company",
#             "transaction_currency",
#             "posting_date",
#             "account_currency",
#         ],
#         filters=gl_filters,
#         order_by="posting_date asc",
#     )

#     for e in gl_entries:
#         if getattr(e, "company", None):
#             e.company_currency = frappe.get_cached_value("Company", e.company, "default_currency")
#         else:
#             e.company_currency = "INR"

#     gl_map = {}
#     for entry in gl_entries:
#         key = (entry.voucher_type, entry.voucher_no)
#         gl_map.setdefault(key, []).append(entry)
#     return gl_map


# def execute(filters=None):
#     filters = filters or {}
#     company_filter = filters.get("company")

#     # parse optional doctype filter
#     doctype_filter = set()
#     if filters.get("doctype_filter"):
#         raw = filters["doctype_filter"]
#         if isinstance(raw, list):
#             doctype_filter = set([d for d in raw if d])
#         else:
#             doctype_filter = set(d.strip() for d in raw.replace("\n", ",").split(",") if d.strip())

#     gl_map = get_gl_entries_by_voucher(company_filter)

#     # Columns
#     columns = [
#         {"label": "Document Type", "fieldname": "doctype", "fieldtype": "Data", "width": 150},
#         {"label": "Document / Item / Payment", "fieldname": "doc_name", "fieldtype": "Dynamic Link", "options": "doctype", "width": 300},
#         {"label": "Reference Doc", "fieldname": "reference_doc", "fieldtype": "Data", "width": 250},

#         {"label": "Company Currency", "fieldname": "company_currency", "fieldtype": "Data", "hidden": 1},
#         {"label": "Txn Currency", "fieldname": "txn_currency", "fieldtype": "Data", "hidden": 1},

#         {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "options": "txn_currency", "width": 120},

#         {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Rounded Total", "fieldname": "rounded_total", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Outstanding Amt", "fieldname": "outstanding_amount", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "options": "txn_currency", "width": 100},
#         {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "options": "txn_currency", "width": 120},

#         {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 200},
#         {"label": "GL Entry", "fieldname": "gl_entry", "fieldtype": "Data", "width": 250},
#         {"label": "Currency", "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 100},

#         {"label": "Exchange Rate", "fieldname": "exchange_rate", "fieldtype": "Float", "width": 100},

#         {"label": "Amount (Local)", "fieldname": "amount_local", "fieldtype": "Currency", "options": "company_currency", "width": 120},
#         {"label": "Amount (Reporting)", "fieldname": "amount_reporting", "fieldtype": "Currency", "options": "INR", "width": 120},

#         # ✅ Fixed: Amount (Transaction) uses the document’s currency dynamically
#         {"label": "Amount (Transaction)", "fieldname": "amount_transaction", "fieldtype": "Currency", "options": "currency", "width": 120},

#         {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 180},
#         {"label": "Account Effect", "fieldname": "account_effect", "fieldtype": "Data", "width": 120},

#         {"label": "Transaction Date", "fieldname": "txn_date", "fieldtype": "Date", "width": 120},
#         {"label": "Document Creation Date", "fieldname": "doc_creation_date", "fieldtype": "Date", "width": 150},

#         {"label": "Bank Account", "fieldname": "bank_account_txn", "fieldtype": "Link", "options": "Bank Account", "width": 150},
#         {"label": "Allocated Amount", "fieldname": "allocated_amount", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Deposit", "fieldname": "deposit", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Withdrawal", "fieldname": "withdrawal", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
#         {"label": "Reference Number", "fieldname": "cheque_no", "fieldtype": "Data", "width": 150},
#         {"label": "Reference Date", "fieldname": "custom_document_creation_date_", "fieldtype": "Date", "width": 120},
#     ]


#     data = []
#     doc_totals = {}

#     bank_txn_meta_fields = [f.fieldname for f in frappe.get_meta("Bank Transaction").fields]
#     has_ref_fields = "reference_doctype" in bank_txn_meta_fields and "reference_name" in bank_txn_meta_fields

#     bank_txn_fields = ["date", "bank_account", "allocated_amount", "deposit", "withdrawal", "reference_number"]
#     if "reference_date" in bank_txn_meta_fields:
#         bank_txn_fields.append("reference_date")

#     doctypes = [
#         {"doctype": "Sales Invoice", "item_table": "Sales Invoice Item"},
#         {"doctype": "Purchase Invoice", "item_table": "Purchase Invoice Item"},
#         {"doctype": "Journal Entry", "item_table": "Journal Entry Account"},
#         {"doctype": "Purchase Receipt", "item_table": "Purchase Receipt Item"},
#         {"doctype": "Delivery Note", "item_table": "Delivery Note Item"},
#         {"doctype": "Sales Order", "item_table": "Sales Order Item"},
#         {"doctype": "Purchase Order", "item_table": "Purchase Order Item"},
#         {"doctype": "Expense Claim", "item_table": "Expense Claim Detail"},
#     ]

#     for dt in doctypes:
#         doctype = dt["doctype"]
#         item_table = dt.get("item_table")

#         if doctype_filter and doctype not in doctype_filter:
#             continue

#         try:
#             meta = frappe.get_meta(doctype)
#         except frappe.DoesNotExistError:
#             continue

#         available_fields = [df.fieldname for df in meta.fields]
#         fields = ["name"]

#         # include company and monetary fields when present
#         if "company" in available_fields:
#             fields.append("company")
#         if "grand_total" in available_fields:
#             fields.append("grand_total")
#         if "rounded_total" in available_fields:
#             fields.append("rounded_total")
#         if "outstanding_amount" in available_fields:
#             fields.append("outstanding_amount")
#         if "currency" in available_fields:
#             fields.append("currency")
#         if "conversion_rate" in available_fields:
#             fields.append("conversion_rate")

#         # include custom_document_creation_date_ if available (needed for Document Creation Date for Journal Entry)
#         if "custom_document_creation_date_" in available_fields:
#             fields.append("custom_document_creation_date_")

#         # include a suitable date field and remember which one
#         date_field = None
#         if "posting_date" in available_fields:
#             date_field = "posting_date"
#         elif "transaction_date" in available_fields:
#             date_field = "transaction_date"
#         if date_field and date_field not in fields:
#             fields.append(date_field)

#         if doctype == "Journal Entry":
#             fields += ["total_debit", "total_credit"]
#         if doctype in ["Sales Order", "Purchase Order"]:
#             if "transaction_date" not in fields and "transaction_date" in available_fields:
#                 fields.append("transaction_date")
#             if "currency" not in fields and "currency" in available_fields:
#                 fields.append("currency")
#             if "conversion_rate" not in fields and "conversion_rate" in available_fields:
#                 fields.append("conversion_rate")
#         if doctype == "Sales Order":
#             if "selling_price_list" in available_fields:
#                 fields.append("selling_price_list")

#         doc_totals[doctype] = 0.0

#         # filters
#         filters_dict = {"docstatus": 1}
#         if "company" in available_fields and company_filter:
#             filters_dict["company"] = company_filter
#         if date_field and filters and filters.get("from_date") and filters.get("to_date"):
#             filters_dict[date_field] = ["between", [filters["from_date"], filters["to_date"]]]

#         records = frappe.get_all(doctype, filters=filters_dict, fields=fields, ignore_permissions=True)

#         for rec in records:
#             name = rec.get("name")
#             grand_total = rec.get("grand_total")
#             rounded_total = rec.get("rounded_total")
#             outstanding = rec.get("outstanding_amount")
#             total_debit = rec.get("total_debit")
#             total_credit = rec.get("total_credit")
#             currency = rec.get("currency")
#             if not currency:
#                 default_company = rec.get("company") or frappe.db.get_default("company")
#                 currency = frappe.get_cached_value("Company", default_company, "default_currency") if default_company else "INR"

#             selling_price_list = rec.get("selling_price_list") if doctype == "Sales Order" else None

#             # Decide document date for FX
#             doc_date = rec.get(date_field) if date_field else None
#             txn_date = rec.get("transaction_date") if "transaction_date" in rec else (rec.get("posting_date") if "posting_date" in rec else None)

#             # Base amounts in document currency
#             if doctype == "Journal Entry":
#                 amount_currency_doc = grand_total or total_debit or 0.0
#             else:
#                 amount_currency_doc = grand_total or 0.0

#             # Determine exchange_rate from document if available (use conversion_rate when present)
#             if "conversion_rate" in available_fields:
#                 conversion_rate = rec.get("conversion_rate") or 1
#             else:
#                 conversion_rate = 1

#             # Reporting (INR) conversion (use document date)
#             rate_to_inr = get_rate_to_inr(currency, doc_date)
#             amount_reporting = amount_currency_doc * rate_to_inr  # ALWAYS INR

#             # amount_local (company currency) using conversion_rate when available
#             # company default currency:
#             company_name = rec.get("company") if "company" in rec else frappe.db.get_default("company")
#             company_currency = frappe.get_cached_value("Company", company_name, "default_currency") if company_name else "INR"

#             # Convert document amounts to company currency for display columns:
#             if currency and company_currency and currency != company_currency:
#                 # Prefer conversion_rate from document if present (document currency -> company currency)
#                 # conversion_rate means: 1 doc_currency = conversion_rate company_currency
#                 amount_in_company = amount_currency_doc * (conversion_rate or 1)
#             else:
#                 amount_in_company = amount_currency_doc

#             # Final amounts for the main (parent) row:
#             amount_local = amount_in_company                       # company currency
#             amount_transaction = amount_currency_doc              # keep in document currency
#             # amount_currency removed / unused

#             if grand_total:
#                 doc_totals[doctype] += grand_total
#             elif total_debit:
#                 doc_totals[doctype] += total_debit

#             # Build reference_doc from child tables where applicable
#             reference_doc = None
#             if doctype in ["Sales Invoice", "Purchase Invoice", "Purchase Receipt", "Delivery Note"]:
#                 child_table = {
#                     "Sales Invoice": ("Sales Invoice Item", "sales_order"),
#                     "Purchase Invoice": ("Purchase Invoice Item", "purchase_order"),
#                     "Purchase Receipt": ("Purchase Receipt Item", "sales_order"),
#                     "Delivery Note": ("Delivery Note Item", "against_sales_order"),
#                 }
#                 item_table, reference_field = child_table[doctype]
#                 references = frappe.get_all(item_table, filters={"parent": name}, fields=[reference_field])
#                 ref_set = set([r[reference_field] for r in references if r.get(reference_field)])
#                 reference_doc = ", ".join(ref_set) if ref_set else None

#             # Use "Main" for parent rows
#             base_row = {
#                 "doctype": doctype,          # used by Dynamic Link column
#                 "doc_name": name,           # actual doc name (clickable)
#                 "reference_doc": reference_doc,

#                 "grand_total": grand_total,
#                 "rounded_total": rounded_total,
#                 "outstanding_amount": outstanding,

#                 "rate": conversion_rate if conversion_rate else None,

#                 "amount_local": amount_local,
#                 "amount_reporting": amount_reporting,
#                 "amount_transaction": amount_transaction,

#                 "amount": None,
#                 "account": None,
#                 "debit": None,
#                 "credit": None,
#                 "total_debit": total_debit,
#                 "total_credit": total_credit,
#                 "gl_entry": None,
#                 "txn_date": txn_date,

#                 # New field: Document Creation Date (custom_document_creation_date_ for Journal Entry)
#                 "doc_creation_date": rec.get("custom_document_creation_date_") if doctype == "Journal Entry" and rec.get("custom_document_creation_date_") else None,

#                 "bank_account_txn": None,
#                 "allocated_amount": None,
#                 "deposit": None,
#                 "withdrawal": None,
#                 "cheque_no": None,
#                 "custom_document_creation_date_": None,

#                 # currency helpers
#                 "currency": currency,               # visible column (doc currency)
#                 "txn_currency": currency,           # used by txn columns
#                 "company_currency": company_currency,  # used by company columns (column 'options' refer to this)
#                 "selling_price_list": selling_price_list,
#                 "exchange_rate": conversion_rate,
#                 "company": company_name,
#                 "account_effect": "Main",
#                 "indent": 0,
#             }
#             data.append(base_row)

#             # --- GL Entry detail lines ---
#             # For child GL rows we want:
#             # - amount_local: company currency (signed_amount)
#             # - amount_reporting: INR (signed_amount * rate_company_to_inr)
#             # - amount_transaction: in the parent's document currency (converted from signed_amount using parent's conversion_rate)
#             for gle in gl_map.get((doctype, name), []):
#                 signed_amount = (gle.debit or 0.0) - (gle.credit or 0.0)  # signed amount in gle.company's company currency

#                 # GL row currency detection (account_currency or transaction_currency on GL entry)
#                 row_currency = getattr(gle, "account_currency", None) or getattr(gle, "transaction_currency", None)
#                 gl_company = gle.company if getattr(gle, "company", None) else company_name
#                 company_currency_gl = frappe.get_cached_value("Company", gl_company, "default_currency") if gl_company else "INR"

#                 # Determine exchange rate from row currency to company currency for this GL row if available
#                 if row_currency and row_currency != company_currency_gl and (
#                     getattr(gle, "debit_in_account_currency", None) is not None
#                     or getattr(gle, "credit_in_account_currency", None) is not None
#                 ):
#                     amount_currency_gl = (gle.debit_in_account_currency or 0.0) - (gle.credit_in_account_currency or 0.0)
#                     if amount_currency_gl:
#                         exchange_rate_row_to_company = abs(signed_amount) / abs(amount_currency_gl)
#                     else:
#                         exchange_rate_row_to_company = 1.0
#                 else:
#                     exchange_rate_row_to_company = 1.0
#                     amount_currency_gl = signed_amount
#                     # For Journal Entry account-specific exchange_rate (Journal Entry Account table)
#                     if doctype == "Journal Entry" and row_currency and row_currency != company_currency_gl:
#                         jea_rate = frappe.db.get_value(
#                             "Journal Entry Account",
#                             {"parent": gle.voucher_no, "account": gle.account},
#                             "exchange_rate",
#                         ) or 0
#                         if jea_rate:
#                             exchange_rate_row_to_company = jea_rate
#                             amount_currency_gl = signed_amount / jea_rate

#                 # Reporting (INR) for GL row
#                 rate_company_to_inr = get_rate_to_inr(company_currency_gl, getattr(gle, "posting_date", None) or doc_date)
#                 amount_reporting_gl = signed_amount * rate_company_to_inr

#                 # Determine display currency and amount_local_gl
#                 if row_currency and row_currency != company_currency_gl:
#                     # GL entry has amounts in account currency fields
#                     debit_val = gle.debit_in_account_currency or 0.0
#                     credit_val = gle.credit_in_account_currency or 0.0
#                     amount_local_gl = debit_val - credit_val  # this is in row_currency
#                     display_currency = row_currency
#                     # However signed_amount is still company-currency equivalent (for amount_reporting)
#                     # We'll keep amount_local column showing signed_amount (company currency) for consistency
#                     # and set txn_currency/display to parent doc currency below
#                 else:
#                     debit_val = gle.debit or 0.0
#                     credit_val = gle.credit or 0.0
#                     amount_local_gl = debit_val - credit_val  # company currency
#                     display_currency = company_currency_gl

#                 # Convert GL signed_amount (company currency) to parent document currency for amount_transaction
#                 # Parent document's conversion rate (1 doc_currency = conversion_rate company_currency)
#                 parent_conv = conversion_rate or 1
#                 try:
#                     # If parent's conversion_rate is provided: doc_amount = company_amount / conversion_rate
#                     # If conversion_rate is 0 or None, fallback to signed_amount (company currency)
#                     if parent_conv:
#                         amount_transaction_gl = signed_amount / parent_conv
#                     else:
#                         amount_transaction_gl = signed_amount
#                 except Exception:
#                     amount_transaction_gl = signed_amount

#                 # Use parent's currency for the txn column
#                 parent_txn_currency = currency

#                 data.append({
#                     "doctype": "GL Entry",
#                     "doc_name": gle.name,
#                     "reference_doc": name,

#                     "account": gle.account,
#                     "debit": debit_val,
#                     "credit": credit_val,

#                     # amount_local: show in company currency (signed_amount)
#                     "amount_local": signed_amount,
#                     "amount_reporting": amount_reporting_gl,
#                     # amount_transaction: converted to parent's document currency
#                     "amount_transaction": amount_transaction_gl,

#                     "gl_entry": get_link_to_form("GL Entry", gle.name),

#                     "company": gl_company,
#                     "account_effect": "Yes",

#                     # currency helpers
#                     # Show txn_currency as parent's currency so the UI displays correct currency symbol
#                     "currency": display_currency,
#                     "txn_currency": parent_txn_currency,
#                     "company_currency": company_currency_gl,
#                     "exchange_rate": exchange_rate_row_to_company,

#                     # show GL posting date in txn_date
#                     "txn_date": gle.posting_date,
#                     # GL / child rows do not show doc_creation_date
#                     "doc_creation_date": None,

#                     "indent": 1,
#                 })

#             # --- Payment Entries linked to this document ---
#             payment_refs = frappe.get_all(
#                 "Payment Entry Reference",
#                 fields=["parent"],
#                 filters={"reference_doctype": doctype, "reference_name": name, "docstatus": 1},
#             )

#             for pref in payment_refs:
#                 payment_entry = frappe.get_doc("Payment Entry", pref.parent)
#                 if company_filter and payment_entry.company != company_filter:
#                     continue
#                 if doctype_filter and doctype not in doctype_filter:
#                     continue

#                 payment_currency = None
#                 if getattr(payment_entry, "paid_from_account_currency", None):
#                     payment_currency = payment_entry.paid_from_account_currency
#                 elif getattr(payment_entry, "paid_to_account_currency", None):
#                     payment_currency = payment_entry.paid_to_account_currency
#                 elif getattr(payment_entry, "paid_from", None):
#                     try:
#                         payment_currency = frappe.get_cached_value("Account", payment_entry.paid_from, "account_currency")
#                     except Exception:
#                         payment_currency = None

#                 if not payment_currency:
#                     payment_currency = frappe.get_cached_value("Company", payment_entry.company, "default_currency")

#                 company_currency_pe = frappe.get_cached_value("Company", payment_entry.company, "default_currency")
#                 rate_to_inr_pe = get_rate_to_inr(payment_currency, payment_entry.posting_date)

#                 amount_currency_pe = payment_entry.paid_amount or 0.0
#                 local_rate = getattr(payment_entry, "source_exchange_rate", 1.0) or 1.0
#                 amount_local_pe = amount_currency_pe * local_rate
#                 amount_reporting_pe = amount_currency_pe * rate_to_inr_pe

#                 # For Payment child rows:
#                 # - amount_transaction should be in payment currency (payment_currency)
#                 # - amount_local is company-currency equivalent (amount_local_pe)
#                 data.append({
#                     "doctype": "Payment Entry",
#                     "doc_name": payment_entry.name,
#                     "reference_doc": name,

#                     "grand_total": payment_entry.paid_amount,
#                     "account": payment_entry.paid_from if getattr(payment_entry, "payment_type", None) == "Receive" else payment_entry.paid_to,

#                     "amount_local": amount_local_pe,
#                     "amount_reporting": amount_reporting_pe,
#                     "amount_transaction": amount_currency_pe,

#                     "txn_date": payment_entry.posting_date,
#                     # Payment child rows do not show doc_creation_date
#                     "doc_creation_date": None,

#                     "cheque_no": payment_entry.reference_no,
#                     "custom_document_creation_date_": payment_entry.reference_date,
#                     "company": payment_entry.company,
#                     "account_effect": "Yes",

#                     # currency helpers
#                     "currency": payment_currency,
#                     "txn_currency": payment_currency,
#                     "company_currency": company_currency_pe,
#                     "exchange_rate": local_rate,

#                     "indent": 1,
#                 })

#     chart = {
#         "data": {
#             "labels": list(doc_totals.keys()),
#             "datasets": [{"values": list(doc_totals.values())}],
#         },
#         "type": "pie",
#         "height": 300,
#     }

#     cumulative_total = sum(doc_totals.values())
#     report_summary = [{
#         "value": cumulative_total,
#         "indicator": "Green" if cumulative_total >= 0 else "Red",
#         "label": "Cumulative Total",
#         "datatype": "Currency",
#         "currency": frappe.get_cached_value('Company', frappe.db.get_default('company'), 'default_currency')
#             if frappe.db.get_default('company') else ""
#     }]

#     return columns, data, None, chart, report_summary












from __future__ import unicode_literals
import frappe
from frappe.utils import getdate, flt, get_link_to_form


# --- FX helper: convert any currency to INR on/before a given date ---
def get_rate_to_inr(from_currency: str, on_date=None) -> float:
    if not from_currency or from_currency == "INR":
        return 1.0

    date = getdate(on_date) if on_date else getdate()

    try:
        from erpnext.setup.utils import get_exchange_rate as erp_get_rate
        r = flt(erp_get_rate(from_currency, "INR", date))
        if r:
            return r
        r_rev = flt(erp_get_rate("INR", from_currency, date))
        if r_rev:
            return 1.0 / r_rev
    except Exception:
        pass

    rate = frappe.db.get_value(
        "Currency Exchange",
        {"from_currency": from_currency, "to_currency": "INR", "date": ["<=", date]},
        "exchange_rate",
        order_by="date desc",
    )
    if rate:
        return flt(rate)

    rev = frappe.db.get_value(
        "Currency Exchange",
        {"from_currency": "INR", "to_currency": from_currency, "date": ["<=", date]},
        "exchange_rate",
        order_by="date desc",
    )
    if rev:
        return 1.0 / flt(rev)

    return 1.0


def get_gl_entries_by_voucher(company=None):
    gl_filters = {"docstatus": 1}
    if company:
        gl_filters["company"] = company

    gl_entries = frappe.get_all(
        "GL Entry",
        fields=[
            "voucher_type",
            "voucher_no",
            "account",
            "debit",
            "credit",
            "debit_in_account_currency",
            "credit_in_account_currency",
            "name",
            "company",
            "transaction_currency",
            "posting_date",
            "account_currency",
        ],
        filters=gl_filters,
        order_by="posting_date asc",
    )

    for e in gl_entries:
        if getattr(e, "company", None):
            e.company_currency = frappe.get_cached_value("Company", e.company, "default_currency")
        else:
            e.company_currency = "INR"

    gl_map = {}
    for entry in gl_entries:
        key = (entry.voucher_type, entry.voucher_no)
        gl_map.setdefault(key, []).append(entry)
    return gl_map


def execute(filters=None):
    filters = filters or {}
    company_filter = filters.get("company")

    # parse optional doctype filter
    doctype_filter = set()
    if filters.get("doctype_filter"):
        raw = filters["doctype_filter"]
        if isinstance(raw, list):
            doctype_filter = set([d for d in raw if d])
        else:
            doctype_filter = set(d.strip() for d in raw.replace("\n", ",").split(",") if d.strip())

    gl_map = get_gl_entries_by_voucher(company_filter)

    # Columns
    columns = [
        {"label": "Document Type", "fieldname": "doctype", "fieldtype": "Data", "width": 150},
        {"label": "Document / Item / Payment", "fieldname": "doc_name", "fieldtype": "Dynamic Link", "options": "doctype", "width": 300},
        {"label": "Reference Doc", "fieldname": "reference_doc", "fieldtype": "Data", "width": 250},

        {"label": "Company Currency", "fieldname": "company_currency", "fieldtype": "Data", "hidden": 1},
        {"label": "Txn Currency", "fieldname": "txn_currency", "fieldtype": "Data", "hidden": 1},

        {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
        {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "options": "txn_currency", "width": 120},

        {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
        {"label": "Rounded Total", "fieldname": "rounded_total", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
        {"label": "Outstanding Amt", "fieldname": "outstanding_amount", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
        {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "options": "txn_currency", "width": 100},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "options": "txn_currency", "width": 120},

        {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 200},
        {"label": "GL Entry", "fieldname": "gl_entry", "fieldtype": "Data", "width": 250},
        {"label": "Currency", "fieldname": "currency", "fieldtype": "Link", "options": "Currency", "width": 100},

        {"label": "Exchange Rate", "fieldname": "exchange_rate", "fieldtype": "Float", "width": 100},

        # NEW: Amount in document/row currency (display column)
        {"label": "Amount (Currency)", "fieldname": "amount_currency", "fieldtype": "Currency", "options": "currency", "width": 120},

        {"label": "Amount (Local)", "fieldname": "amount_local", "fieldtype": "Currency", "options": "company_currency", "width": 120},
        {"label": "Amount (Reporting)", "fieldname": "amount_reporting", "fieldtype": "Currency", "options": "INR", "width": 120},

        {"label": "Amount (Transaction)", "fieldname": "amount_transaction", "fieldtype": "Currency", "options": "currency", "width": 140},

        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 180},
        {"label": "Account Effect", "fieldname": "account_effect", "fieldtype": "Data", "width": 120},

        {"label": "Transaction Date", "fieldname": "txn_date", "fieldtype": "Date", "width": 120},
        {"label": "Document Creation Date", "fieldname": "doc_creation_date", "fieldtype": "Date", "width": 150},

        {"label": "Bank Account", "fieldname": "bank_account_txn", "fieldtype": "Link", "options": "Bank Account", "width": 150},
        {"label": "Allocated Amount", "fieldname": "allocated_amount", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
        {"label": "Deposit", "fieldname": "deposit", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
        {"label": "Withdrawal", "fieldname": "withdrawal", "fieldtype": "Currency", "options": "txn_currency", "width": 120},
        {"label": "Reference Number", "fieldname": "cheque_no", "fieldtype": "Data", "width": 150},
        {"label": "Reference Date", "fieldname": "custom_document_creation_date_", "fieldtype": "Date", "width": 120},
    ]

    data = []
    doc_totals = {}

    bank_txn_meta_fields = [f.fieldname for f in frappe.get_meta("Bank Transaction").fields]
    has_ref_fields = "reference_doctype" in bank_txn_meta_fields and "reference_name" in bank_txn_meta_fields

    bank_txn_fields = ["date", "bank_account", "allocated_amount", "deposit", "withdrawal", "reference_number"]
    if "reference_date" in bank_txn_meta_fields:
        bank_txn_fields.append("reference_date")

    doctypes = [
        {"doctype": "Sales Invoice", "item_table": "Sales Invoice Item"},
        {"doctype": "Purchase Invoice", "item_table": "Purchase Invoice Item"},
        {"doctype": "Journal Entry", "item_table": "Journal Entry Account"},
        {"doctype": "Purchase Receipt", "item_table": "Purchase Receipt Item"},
        {"doctype": "Delivery Note", "item_table": "Delivery Note Item"},
        {"doctype": "Sales Order", "item_table": "Sales Order Item"},
        {"doctype": "Purchase Order", "item_table": "Purchase Order Item"},
        {"doctype": "Expense Claim", "item_table": "Expense Claim Detail"},
    ]

    for dt in doctypes:
        doctype = dt["doctype"]
        item_table = dt.get("item_table")

        if doctype_filter and doctype not in doctype_filter:
            continue

        try:
            meta = frappe.get_meta(doctype)
        except frappe.DoesNotExistError:
            continue

        available_fields = [df.fieldname for df in meta.fields]
        fields = ["name"]

        # include company and monetary fields when present
        if "company" in available_fields:
            fields.append("company")
        if "grand_total" in available_fields:
            fields.append("grand_total")
        if "rounded_total" in available_fields:
            fields.append("rounded_total")
        if "outstanding_amount" in available_fields:
            fields.append("outstanding_amount")
        if "currency" in available_fields:
            fields.append("currency")
        if "conversion_rate" in available_fields:
            fields.append("conversion_rate")

        # include custom_document_creation_date_ if available (needed for Document Creation Date for Journal Entry)
        if "custom_document_creation_date_" in available_fields:
            fields.append("custom_document_creation_date_")

        # include a suitable date field and remember which one
        date_field = None
        if "posting_date" in available_fields:
            date_field = "posting_date"
        elif "transaction_date" in available_fields:
            date_field = "transaction_date"
        if date_field and date_field not in fields:
            fields.append(date_field)

        if doctype == "Journal Entry":
            fields += ["total_debit", "total_credit"]
        if doctype in ["Sales Order", "Purchase Order"]:
            if "transaction_date" not in fields and "transaction_date" in available_fields:
                fields.append("transaction_date")
            if "currency" not in fields and "currency" in available_fields:
                fields.append("currency")
            if "conversion_rate" not in fields and "conversion_rate" in available_fields:
                fields.append("conversion_rate")
        if doctype == "Sales Order":
            if "selling_price_list" in available_fields:
                fields.append("selling_price_list")

        doc_totals[doctype] = 0.0

        # filters
        filters_dict = {"docstatus": 1}
        if "company" in available_fields and company_filter:
            filters_dict["company"] = company_filter
        if date_field and filters and filters.get("from_date") and filters.get("to_date"):
            filters_dict[date_field] = ["between", [filters["from_date"], filters["to_date"]]]

        records = frappe.get_all(doctype, filters=filters_dict, fields=fields, ignore_permissions=True)

        for rec in records:
            name = rec.get("name")
            grand_total = rec.get("grand_total")
            rounded_total = rec.get("rounded_total")
            outstanding = rec.get("outstanding_amount")
            total_debit = rec.get("total_debit")
            total_credit = rec.get("total_credit")
            currency = rec.get("currency")
            if not currency:
                default_company = rec.get("company") or frappe.db.get_default("company")
                currency = frappe.get_cached_value("Company", default_company, "default_currency") if default_company else "INR"

            selling_price_list = rec.get("selling_price_list") if doctype == "Sales Order" else None

            # Decide document date for FX
            doc_date = rec.get(date_field) if date_field else None
            txn_date = rec.get("transaction_date") if "transaction_date" in rec else (rec.get("posting_date") if "posting_date" in rec else None)

            # Base amounts in document currency
            if doctype == "Journal Entry":
                amount_currency_doc = grand_total or total_debit or 0.0
            else:
                amount_currency_doc = grand_total or 0.0

            # Determine exchange_rate from document if available (use conversion_rate when present)
            if "conversion_rate" in available_fields:
                conversion_rate = rec.get("conversion_rate") or 1
            else:
                conversion_rate = 1

            # Reporting (INR) conversion (use document date)
            rate_to_inr = get_rate_to_inr(currency, doc_date)
            amount_reporting = amount_currency_doc * rate_to_inr  # ALWAYS INR

            # amount_local (company currency) using conversion_rate when available
            # company default currency:
            company_name = rec.get("company") if "company" in rec else frappe.db.get_default("company")
            company_currency = frappe.get_cached_value("Company", company_name, "default_currency") if company_name else "INR"

            # Convert document amounts to company currency for display columns:
            if currency and company_currency and currency != company_currency:
                amount_in_company = amount_currency_doc * (conversion_rate or 1)
            else:
                amount_in_company = amount_currency_doc

            # Final amounts for the main (parent) row:
            amount_local = amount_in_company                       # company currency
            amount_transaction = amount_currency_doc              # keep in document currency

            if grand_total:
                doc_totals[doctype] += grand_total
            elif total_debit:
                doc_totals[doctype] += total_debit

            # Build reference_doc from child tables where applicable
            reference_doc = None
            if doctype in ["Sales Invoice", "Purchase Invoice", "Purchase Receipt", "Delivery Note"]:
                child_table = {
                    "Sales Invoice": ("Sales Invoice Item", "sales_order"),
                    "Purchase Invoice": ("Purchase Invoice Item", "purchase_order"),
                    "Purchase Receipt": ("Purchase Receipt Item", "sales_order"),
                    "Delivery Note": ("Delivery Note Item", "against_sales_order"),
                }
                item_table, reference_field = child_table[doctype]
                references = frappe.get_all(item_table, filters={"parent": name}, fields=[reference_field])
                ref_set = set([r[reference_field] for r in references if r.get(reference_field)])
                reference_doc = ", ".join(ref_set) if ref_set else None

            # Use "Main" for parent rows
            base_row = {
                "doctype": doctype,
                "doc_name": name,
                "reference_doc": reference_doc,

                "grand_total": grand_total,
                "rounded_total": rounded_total,
                "outstanding_amount": outstanding,

                "rate": conversion_rate if conversion_rate else None,

                "amount_local": amount_local,
                "amount_reporting": amount_reporting,
                "amount_transaction": amount_transaction,

                # NEW: amount in document currency
                "amount_currency": amount_currency_doc,

                "amount": None,
                "account": None,
                "debit": None,
                "credit": None,
                "total_debit": total_debit,
                "total_credit": total_credit,
                "gl_entry": None,
                "txn_date": txn_date,

                "doc_creation_date": rec.get("custom_document_creation_date_") if doctype == "Journal Entry" and rec.get("custom_document_creation_date_") else None,

                "bank_account_txn": None,
                "allocated_amount": None,
                "deposit": None,
                "withdrawal": None,
                "cheque_no": None,
                "custom_document_creation_date_": None,

                "currency": currency,
                "txn_currency": currency,
                "company_currency": company_currency,
                "selling_price_list": selling_price_list,
                "exchange_rate": conversion_rate,
                "company": company_name,
                "account_effect": "Main",
                "indent": 0,
            }
            data.append(base_row)

            # --- GL Entry detail lines ---
            for gle in gl_map.get((doctype, name), []):
                # signed amount in GL entry (company-currency)
                signed_amount = flt((gle.debit or 0.0) - (gle.credit or 0.0))

                # detect GL row's currency (account_currency / transaction_currency)
                row_currency = getattr(gle, "account_currency", None) or getattr(gle, "transaction_currency", None)
                gl_company = gle.company if getattr(gle, "company", None) else company_name
                company_currency_gl = frappe.get_cached_value("Company", gl_company, "default_currency") if gl_company else "INR"

                # default initializations
                debit_val = flt(gle.debit or 0.0)
                credit_val = flt(gle.credit or 0.0)
                exchange_rate_row_to_company = 1.0
                amount_currency_gl = None
                amount_transaction_gl = None
                txn_currency_for_row = currency  # default to parent doc currency

                # If GL row has its own currency and the account-currency amounts exist, prefer them
                if row_currency and row_currency != company_currency_gl:
                    debit_ac = getattr(gle, "debit_in_account_currency", None)
                    credit_ac = getattr(gle, "credit_in_account_currency", None)

                    if debit_ac is not None or credit_ac is not None:
                        debit_ac = flt(debit_ac or 0.0)
                        credit_ac = flt(credit_ac or 0.0)
                        amount_currency_gl = debit_ac - credit_ac

                        # For display use the GL-row account-currency numbers
                        debit_val = debit_ac
                        credit_val = credit_ac
                        amount_transaction_gl = amount_currency_gl
                        txn_currency_for_row = row_currency

                        try:
                            exchange_rate_row_to_company = abs(signed_amount) / abs(amount_currency_gl) if amount_currency_gl else 1.0
                        except Exception:
                            exchange_rate_row_to_company = 1.0
                    else:
                        # account-currency fields missing on GL Entry object: fallback is used below
                        frappe.log_error(
                            title="GL child: missing account-currency fields",
                            message=f"GLE={getattr(gle,'name',None)}, account_currency={row_currency}, debit={getattr(gle,'debit',None)}, credit={getattr(gle,'credit',None)}, parent_currency={currency}"
                        )

                # Fallback: if account-currency wasn't used, convert company signed_amount -> parent doc currency
                if amount_transaction_gl is None:
                    parent_doc_currency = currency
                    parent_conv = conversion_rate or 1
                    try:
                        if parent_conv:
                            amount_transaction_gl = flt(signed_amount) / flt(parent_conv)
                        else:
                            amount_transaction_gl = flt(signed_amount)
                    except Exception:
                        amount_transaction_gl = flt(signed_amount)
                    txn_currency_for_row = parent_doc_currency

                # Reporting (INR) for GL row
                rate_company_to_inr = get_rate_to_inr(company_currency_gl, getattr(gle, "posting_date", None) or doc_date)
                amount_reporting_gl = signed_amount * rate_company_to_inr

                # Determine display currency (account currency when present otherwise company currency)
                display_currency = row_currency if (row_currency and row_currency != company_currency_gl) else company_currency_gl

                # Append GL child row. Ensure currency/txn_currency match the amount_transaction currency.
                data.append({
                    "doctype": "GL Entry",
                    "doc_name": getattr(gle, "name", None),
                    "reference_doc": name,

                    "account": getattr(gle, "account", None),
                    "debit": debit_val,
                    "credit": credit_val,

                    "amount_local": signed_amount,
                    "amount_reporting": amount_reporting_gl,
                    "amount_transaction": amount_transaction_gl,

                    # NEW: amount in row/document currency
                    "amount_currency": amount_transaction_gl,

                    "gl_entry": get_link_to_form("GL Entry", getattr(gle, "name", None)),

                    "company": gl_company,
                    "account_effect": "Yes",

                    # Must match the currency used for amount_transaction
                    "currency": txn_currency_for_row,
                    "txn_currency": txn_currency_for_row,
                    "company_currency": company_currency_gl,
                    "exchange_rate": exchange_rate_row_to_company,

                    "txn_date": getattr(gle, "posting_date", None),
                    "doc_creation_date": None,

                    "indent": 1,
                })

            # --- Payment Entries linked to this document ---
            payment_refs = frappe.get_all(
                "Payment Entry Reference",
                fields=["parent"],
                filters={"reference_doctype": doctype, "reference_name": name, "docstatus": 1},
            )

            for pref in payment_refs:
                payment_entry = frappe.get_doc("Payment Entry", pref.parent)
                if company_filter and payment_entry.company != company_filter:
                    continue
                if doctype_filter and doctype not in doctype_filter:
                    continue

                payment_currency = None
                if getattr(payment_entry, "paid_from_account_currency", None):
                    payment_currency = payment_entry.paid_from_account_currency
                elif getattr(payment_entry, "paid_to_account_currency", None):
                    payment_currency = payment_entry.paid_to_account_currency
                elif getattr(payment_entry, "paid_from", None):
                    try:
                        payment_currency = frappe.get_cached_value("Account", payment_entry.paid_from, "account_currency")
                    except Exception:
                        payment_currency = None

                if not payment_currency:
                    payment_currency = frappe.get_cached_value("Company", payment_entry.company, "default_currency")

                company_currency_pe = frappe.get_cached_value("Company", payment_entry.company, "default_currency")
                rate_to_inr_pe = get_rate_to_inr(payment_currency, payment_entry.posting_date)

                amount_currency_pe = payment_entry.paid_amount or 0.0
                local_rate = getattr(payment_entry, "source_exchange_rate", 1.0) or 1.0
                amount_local_pe = amount_currency_pe * local_rate
                amount_reporting_pe = amount_currency_pe * rate_to_inr_pe

                data.append({
                    "doctype": "Payment Entry",
                    "doc_name": payment_entry.name,
                    "reference_doc": name,

                    "grand_total": payment_entry.paid_amount,
                    "account": payment_entry.paid_from if getattr(payment_entry, "payment_type", None) == "Receive" else payment_entry.paid_to,

                    "amount_local": amount_local_pe,
                    "amount_reporting": amount_reporting_pe,
                    "amount_transaction": amount_currency_pe,

                    # NEW: amount in payment entry currency
                    "amount_currency": amount_currency_pe,

                    "txn_date": payment_entry.posting_date,
                    "doc_creation_date": None,

                    "cheque_no": payment_entry.reference_no,
                    "custom_document_creation_date_": payment_entry.reference_date,
                    "company": payment_entry.company,
                    "account_effect": "Yes",

                    "currency": payment_currency,
                    "txn_currency": payment_currency,
                    "company_currency": company_currency_pe,
                    "exchange_rate": local_rate,

                    "indent": 1,
                })

    chart = {
        "data": {
            "labels": list(doc_totals.keys()),
            "datasets": [{"values": list(doc_totals.values())}],
        },
        "type": "pie",
        "height": 300,
    }

    cumulative_total = sum(doc_totals.values())
    report_summary = [{
        "value": cumulative_total,
        "indicator": "Green" if cumulative_total >= 0 else "Red",
        "label": "Cumulative Total",
        "datatype": "Currency",
        "currency": frappe.get_cached_value('Company', frappe.db.get_default('company'), 'default_currency')
            if frappe.db.get_default('company') else ""
    }]

    return columns, data, None, chart, report_summary