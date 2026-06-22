from typing import Optional, Union
from pydantic import BaseModel


class PartyInfo(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    swift_code: Optional[str] = None


class BankInfo(BaseModel):
    name: Optional[str] = None
    branch: Optional[str] = None
    swift_code: Optional[str] = None


class InvoiceFields(BaseModel):
    invoice_number: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    beneficiary: Optional[PartyInfo] = None
    applicant: Optional[PartyInfo] = None
    goods_description: Optional[str] = None
    port_of_loading: Optional[str] = None
    port_of_discharge: Optional[str] = None
    shipment_date: Optional[str] = None
    lc_reference: Optional[str] = None


class BillOfLadingFields(BaseModel):
    bl_number: Optional[str] = None
    shipper: Optional[PartyInfo] = None
    consignee: Optional[str] = None  
    vessel_name: Optional[str] = None
    port_of_loading: Optional[str] = None
    port_of_discharge: Optional[str] = None
    goods_description: Optional[str] = None
    shipment_date: Optional[str] = None
    lc_reference: Optional[str] = None


class PackingListFields(BaseModel):
    beneficiary: Optional[PartyInfo] = None
    applicant: Optional[PartyInfo] = None
    goods_description: Optional[str] = None
    quantity: Optional[float] = None
    gross_weight: Optional[float] = None
    net_weight: Optional[float] = None
    number_of_packages: Optional[int] = None
    lc_reference: Optional[str] = None


class CertificateOfOriginFields(BaseModel):
    exporter: Optional[PartyInfo] = None
    consignee: Optional[PartyInfo] = None
    country_of_origin: Optional[str] = None
    goods_description: Optional[str] = None
    quantity: Optional[float] = None
    lc_reference: Optional[str] = None


class InsuranceCertificateFields(BaseModel):
    insured_party: Optional[PartyInfo] = None
    policy_number: Optional[str] = None
    insured_value: Optional[float] = None
    currency: Optional[str] = None
    goods_description: Optional[str] = None
    coverage_type: Optional[str] = None
    lc_reference: Optional[str] = None


class DraftFields(BaseModel):
    drawer: Optional[PartyInfo] = None
    drawee: Optional[BankInfo] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    tenor: Optional[str] = None
    lc_reference: Optional[str] = None


class InspectionCertificateFields(BaseModel):
    inspector: Optional[str] = None
    goods_description: Optional[str] = None
    quantity: Optional[float] = None
    inspection_date: Optional[str] = None
    result: Optional[str] = None
    lc_reference: Optional[str] = None


class LCTermsFields(BaseModel):
    lc_reference: Optional[str] = None
    applicant: Optional[PartyInfo] = None
    beneficiary: Optional[PartyInfo] = None
    issuing_bank: Optional[BankInfo] = None
    advising_bank: Optional[BankInfo] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    goods_description: Optional[str] = None
    port_of_loading: Optional[str] = None
    port_of_discharge: Optional[str] = None
    latest_shipment_date: Optional[str] = None
    expiry_date: Optional[str] = None
    presentation_period: Optional[str] = None
    partial_shipments: Optional[str] = None
    transshipment: Optional[str] = None


FIELD_SCHEMA_MAP = {
    "invoice": InvoiceFields,
    "bill_of_lading": BillOfLadingFields,
    "packing_list": PackingListFields,
    "certificate_of_origin": CertificateOfOriginFields,
    "insurance_certificate": InsuranceCertificateFields,
    "draft": DraftFields,
    "inspection_certificate": InspectionCertificateFields,
    "lc_terms": LCTermsFields,
}