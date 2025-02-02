from algosdk import mnemonic
from algosdk.v2client.algod import *
from algosdk.atomic_transaction_composer import *
from algosdk.future.transaction import *
from algosdk.abi import *
from algosdk.mnemonic import *
from algosdk.account import *

from sandbox import get_accounts

client = AlgodClient("a" * 64, "http://localhost:4001")

with open("../contract.json") as f:
    js = f.read()

c = Contract.from_json(js)

app_id = c.networks["default"].app_id

def get_method(name: str) -> Method:
    for m in c.methods:
        if m.name == name:
            return m
    raise Exception("No method with the name {}".format(name))


addr, sk = get_accounts()[0]

signer = AccountTransactionSigner(sk)

sp = client.suggested_params()

comp = AtomicTransactionComposer()

comp.add_method_call(app_id, get_method("add"), addr, sp, signer, method_args=[1,1])
comp.add_method_call(app_id, get_method("sub"), addr, sp, signer, method_args=[3,1])
comp.add_method_call(app_id, get_method("div"), addr, sp, signer, method_args=[4,2])
comp.add_method_call(app_id, get_method("mul"), addr, sp, signer, method_args=[3,2])
comp.add_method_call(app_id, get_method("qrem"), addr, sp, signer, method_args=[27,5])
comp.add_method_call(app_id, get_method("reverse"), addr, sp, signer, method_args=["desrever yllufsseccus"])

txn = TransactionWithSigner(PaymentTxn(addr, sp, addr, 10000), signer)
comp.add_method_call(app_id, get_method("txntest"), addr, sp, signer, method_args=[10000, txn, 1000])

comp.add_method_call(app_id, get_method("manyargs"), addr, sp, signer, method_args=[2]*20)

comp.add_method_call(
    app_id,
    get_method("min_bal"),
    addr,
    sp,
    signer,
    method_args=["SKCBRBKPIGY5LI2OU63IE5LMNQ5BVVOKPHWTPPWFQOI4NG4TI35SLAA3JQ"],
)

comp.add_method_call(
   app_id,
   get_method("concat_strings"),
   addr,
   sp,
   signer,
   method_args=[["this", "string", "is", "joined"]]
)


resp = comp.execute(client, 2)

for result in resp.abi_results:
    print(result.return_value)
