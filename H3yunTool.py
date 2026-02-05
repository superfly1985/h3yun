import json
import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

from Web_Service.氚云.src.h3yun_config import H3YunConfig
from Web_Service.氚云.src.h3yun_client import H3YunClient


def apply_env():
    p = ROOT / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s and "=" in s and not s.startswith("#"):
                k, v = s.split("=", 1)
                os.environ[k.strip()] = v.strip()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("H3yunTool")
        apply_env()
        self.cfg = H3YunConfig.from_env()
        self.client = H3YunClient(self.cfg)
        self.config = {}
        self.schema = tk.StringVar()
        self.biz_id = tk.StringVar()
        self.search_field = tk.StringVar()
        self.search_value = tk.StringVar()
        self.edit_field = tk.StringVar()
        self.edit_value = tk.StringVar()
        self.attach_field = tk.StringVar()
        self.full_details = tk.BooleanVar(value=True)
        self.file = tk.StringVar()
        self.dir = tk.StringVar()
        self.out = tk.StringVar()
        fr = tk.Frame(root)
        fr.pack(fill=tk.BOTH, expand=True)
        ttk.Label(fr, text="H3yun Data Manager 氚云数据管理").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        ttk.Button(fr, text="Choose Config 选择配置", command=self.choose_config).grid(row=0, column=1, padx=6, pady=6)
        ttk.Button(fr, text="Quick Save 快速保存", command=self.save_quick).grid(row=0, column=2, padx=6, pady=6)
        ttk.Label(fr, text="Schema 表单编码").grid(row=1, column=0, padx=6, pady=6)
        ttk.Entry(fr, textvariable=self.schema, width=24).grid(row=1, column=1, padx=6, pady=6)
        ttk.Label(fr, text="BizObjectId 业务ID").grid(row=1, column=2, padx=6, pady=6)
        ttk.Entry(fr, textvariable=self.biz_id, width=24).grid(row=1, column=3, padx=6, pady=6)
        ttk.Label(fr, text="Search Field 查询字段").grid(row=2, column=0, padx=6, pady=6)
        ttk.Entry(fr, textvariable=self.search_field, width=24).grid(row=2, column=1, padx=6, pady=6)
        ttk.Label(fr, text="Search Value 查询值").grid(row=2, column=2, padx=6, pady=6)
        ttk.Entry(fr, textvariable=self.search_value, width=24).grid(row=2, column=3, padx=6, pady=6)
        ttk.Button(fr, text="Load One 查询单条", command=self.load_one).grid(row=3, column=0, padx=6, pady=6)
        ttk.Button(fr, text="Load Many 批量查询", command=self.load_many).grid(row=3, column=1, padx=6, pady=6)
        ttk.Checkbutton(fr, text="Full Details 全字段", variable=self.full_details).grid(row=3, column=2, padx=6, pady=6)
        ttk.Label(fr, text="Edit Field 编辑字段").grid(row=4, column=0, padx=6, pady=6)
        ttk.Entry(fr, textvariable=self.edit_field, width=24).grid(row=4, column=1, padx=6, pady=6)
        ttk.Label(fr, text="Edit Value 编辑值").grid(row=4, column=2, padx=6, pady=6)
        ttk.Entry(fr, textvariable=self.edit_value, width=24).grid(row=4, column=3, padx=6, pady=6)
        ttk.Button(fr, text="Update 更新", command=self.update_one).grid(row=5, column=0, padx=6, pady=6)
        ttk.Button(fr, text="Remove 删除", command=self.remove_one).grid(row=5, column=1, padx=6, pady=6)
        ttk.Button(fr, text="Create 新增", command=self.open_create_dialog).grid(row=5, column=2, padx=6, pady=6)
        ttk.Label(fr, text="Attachment Field 附件字段").grid(row=6, column=0, padx=6, pady=6)
        ttk.Entry(fr, textvariable=self.attach_field, width=24).grid(row=6, column=1, padx=6, pady=6)
        ttk.Button(fr, text="Choose File 选择文件", command=self.choose_file).grid(row=6, column=2, padx=6, pady=6)
        ttk.Button(fr, text="Choose Dir 选择目录", command=self.choose_dir).grid(row=6, column=3, padx=6, pady=6)
        ttk.Label(fr, text="Output Dir 输出目录").grid(row=7, column=0, padx=6, pady=6)
        ttk.Entry(fr, textvariable=self.out, width=24).grid(row=7, column=1, padx=6, pady=6)
        ttk.Button(fr, text="Choose Out 选择输出", command=self.choose_out).grid(row=7, column=2, padx=6, pady=6)
        ttk.Button(fr, text="Upload 上传附件", command=self.upload).grid(row=7, column=3, padx=6, pady=6)
        ttk.Button(fr, text="Download 下载附件", command=self.download).grid(row=7, column=4, padx=6, pady=6)
        self.table = ttk.Treeview(fr, columns=("col1"), show="headings")
        self.table.grid(row=8, column=0, columnspan=4, padx=6, pady=6, sticky="nsew")
        self.vsb = ttk.Scrollbar(fr, orient="vertical", command=self.table.yview)
        self.vsb.grid(row=8, column=4, sticky="ns")
        self.hsb = ttk.Scrollbar(fr, orient="horizontal", command=self.table.xview)
        self.hsb.grid(row=9, column=0, columnspan=4, sticky="ew")
        self.table.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.table.bind('<<TreeviewSelect>>', self.on_select_row)
        self.table.bind('<ButtonRelease-1>', self.on_click_cell)
        fr.grid_columnconfigure(0, weight=1)
        fr.grid_columnconfigure(1, weight=1)
        fr.grid_columnconfigure(2, weight=1)
        fr.grid_columnconfigure(3, weight=1)
        fr.grid_rowconfigure(8, weight=1)
        self.apply_cfg()
        self.load_default_config()
        self.schema.trace_add('write', lambda *a: self.save_persist())
        self.biz_id.trace_add('write', lambda *a: self.save_persist())
        self.edit_field.trace_add('write', lambda *a: self.save_persist())
        self.attach_field.trace_add('write', lambda *a: self.save_persist())
        self.dir.trace_add('write', lambda *a: self.save_persist())
        self.out.trace_add('write', lambda *a: self.save_persist())

    def choose_config(self):
        p = filedialog.askopenfilename()
        if not p:
            return
        try:
            self.config = json.loads(Path(p).read_text(encoding="utf-8"))
            self.apply_cfg()
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def apply_cfg(self):
        self.schema.set(self.config.get("schema", self.schema.get()))
        self.biz_id.set(self.config.get("id", self.biz_id.get()))
        up = self.config.get("upload", {})
        dn = self.config.get("download", {})
        self.dir.set(up.get("dir", self.dir.get()))
        self.out.set(dn.get("out", self.out.get()))
        if isinstance(self.config.get("full_details"), bool):
            self.full_details.set(self.config.get("full_details"))

    def build_config(self):
        return {
            "schema": self.schema.get(),
            "id": self.biz_id.get(),
            "attach_field": self.attach_field.get(),
            "full_details": bool(self.full_details.get()),
            "search": {"field": self.search_field.get(), "value": self.search_value.get()},
            "edit": {"field": self.edit_field.get(), "value": self.edit_value.get()},
            "upload": {"dir": self.dir.get(), "patterns": ["*.png", "*.jpg"]},
            "download": {"out": self.out.get()},
        }

    def load_default_config(self):
        p = ROOT / "h3yun.config.json"
        if p.exists():
            try:
                self.config = json.loads(p.read_text(encoding="utf-8"))
                self.apply_cfg()
            except Exception:
                pass

    def save_quick(self):
        d = self.build_config()
        p = ROOT / ".h3yun.quick.json"
        try:
            p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def save_persist(self):
        d = self.build_config()
        p = ROOT / "h3yun.config.json"
        try:
            p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def choose_file(self):
        p = filedialog.askopenfilename()
        if p:
            self.file.set(p)

    def choose_dir(self):
        p = filedialog.askdirectory()
        if p:
            self.dir.set(p)
            self.save_persist()

    def choose_out(self):
        p = filedialog.askdirectory()
        if p:
            self.out.set(p)
            self.save_persist()

    def open_create_dialog(self):
        win = tk.Toplevel(self.root)
        win.title("Create 新增")
        cols = list(self.table["columns"]) or []
        exclude = {"ObjectId","CreatedBy","OwnerId","OwnerDeptId","CreatedTime","ModifiedTime","Status","CreatedByObject","OwnerIdObject","OwnerDeptIdObject"}
        fields = [c for c in cols if c not in exclude]
        if not fields:
            fields = [f for f in ["Name", self.attach_field.get()] if f]
        entries = {}
        r = 0
        for f in fields:
            ttk.Label(win, text=f).grid(row=r, column=0, padx=6, pady=4, sticky="e")
            e = ttk.Entry(win, width=32)
            e.grid(row=r, column=1, padx=6, pady=4)
            entries[f] = e
            r += 1
        def submit():
            data = {}
            for k, ent in entries.items():
                data[k] = ent.get()
            try:
                res = self.client.create_biz_object(self.schema.get(), data, True)
                rid = ((res.get("ReturnData") or {}).get("BizObjectId") or (res.get("ReturnData") or {}).get("ObjectId"))
                if rid:
                    self.biz_id.set(rid)
                    self.load_one()
                win.destroy()
            except Exception as e:
                messagebox.showerror("错误", str(e))
        ttk.Button(win, text="Submit 提交", command=submit).grid(row=r, column=0, padx=6, pady=8)
        ttk.Button(win, text="Cancel 取消", command=win.destroy).grid(row=r, column=1, padx=6, pady=8)


    def load_one(self):
        r = self.client.load_biz_object(self.schema.get(), self.biz_id.get())
        d = (r.get("ReturnData") or {}).get("BizObject") or {}
        base_pref = ["ObjectId", "Name", self.attach_field.get(), "CreatedBy", "OwnerId", "OwnerDeptId", "CreatedTime", "ModifiedTime", "Status", "CreatedByObject", "OwnerIdObject", "OwnerDeptIdObject"]
        preferred = [f for f in base_pref if f and f in d]
        cols = preferred + [k for k in d.keys() if k not in preferred]
        if not cols:
            cols = ["ObjectId"]
        self.table.configure(columns=cols)
        for c in cols:
            self.table.heading(c, text=c, command=(lambda cc=c: self.set_edit_field(cc)))
        for i in self.table.get_children():
            self.table.delete(i)
        def fmt(v):
            if isinstance(v, dict):
                return v.get("Name") or json.dumps(v, ensure_ascii=False)
            if isinstance(v, list):
                return json.dumps(v, ensure_ascii=False)
            return v if v is not None else ""
        vals = [fmt(d.get(c)) for c in cols]
        self.table.insert("", "end", values=vals)

    def on_select_row(self, event):
        sel = self.table.selection()
        if not sel:
            return
        item = sel[0]
        cols = list(self.table["columns"]) or []
        vals = self.table.item(item, 'values') or []
        if "ObjectId" in cols:
            idx = cols.index("ObjectId")
            if idx < len(vals):
                self.biz_id.set(vals[idx])

    def on_click_cell(self, event):
        row_id = self.table.identify_row(event.y)
        col_id = self.table.identify_column(event.x)
        if not row_id or not col_id:
            return
        try:
            ci = int(col_id.replace('#','')) - 1
        except Exception:
            return
        cols = list(self.table["columns"]) or []
        if ci < 0 or ci >= len(cols):
            return
        col = cols[ci]
        vals = self.table.item(row_id, 'values') or []
        val = vals[ci] if ci < len(vals) else ""
        self.edit_field.set(col)
        self.edit_value.set(val)
        self.attach_field.set(col)

    def set_edit_field(self, col):
        self.edit_field.set(col)
        self.attach_field.set(col)

    def load_many(self):
        matcher = {"Type": "And", "Matchers": []}
        if self.search_field.get() and self.search_value.get():
            matcher = {"Type": "And", "Matchers": [{"Type": "Equal", "Left": self.search_field.get(), "Right": self.search_value.get()}]}
        fobj = {
            "FromRowNum": 0,
            "RequireCount": True,
            "ReturnItems": [x for x in ["ObjectId","Name",self.attach_field.get()] if x],
            "SortByCollection": [],
            "ToRowNum": 200,
            "Matcher": matcher,
        }
        params = {"Filter": json.dumps(fobj, ensure_ascii=False, separators=(",", ":"))}
        r = self.client.load_biz_objects(self.schema.get(), params)
        arr = (r.get("ReturnData") or {}).get("BizObjectArray") or []
        if self.full_details.get():
            full_arr = []
            for o in arr:
                oid = o.get("ObjectId")
                if oid:
                    rr = self.client.load_biz_object(self.schema.get(), oid)
                    bo = (rr.get("ReturnData") or {}).get("BizObject") or {}
                    full_arr.append(bo)
            arr = full_arr
        for o in arr:
            if isinstance(o.get("CreatedByObject"), dict):
                o["CreatedByName"] = o["CreatedByObject"].get("Name")
            if isinstance(o.get("OwnerIdObject"), dict):
                o["OwnerIdName"] = o["OwnerIdObject"].get("Name")
            if isinstance(o.get("OwnerDeptIdObject"), dict):
                o["OwnerDeptName"] = o["OwnerDeptIdObject"].get("Name")
        colset = set()
        for o in arr:
            if isinstance(o, dict):
                colset.update(o.keys())
        base_pref = ["ObjectId", "Name", self.attach_field.get(), "CreatedBy", "OwnerId", "OwnerDeptId", "CreatedTime", "ModifiedTime", "Status", "CreatedByName", "OwnerIdName", "OwnerDeptName"]
        preferred = [f for f in base_pref if f and f in colset]
        cols = preferred + [k for k in sorted(colset) if k not in preferred]
        if not cols:
            cols = ["ObjectId"]
        self.table.configure(columns=cols)
        for c in cols:
            self.table.heading(c, text=c, command=(lambda cc=c: self.set_edit_field(cc)))
        for i in self.table.get_children():
            self.table.delete(i)
        def fmt(v):
            if isinstance(v, dict):
                return v.get("Name") or json.dumps(v, ensure_ascii=False)
            if isinstance(v, list):
                return json.dumps(v, ensure_ascii=False)
            return v if v is not None else ""
        for o in arr:
            vals = [fmt(o.get(c)) for c in cols]
            self.table.insert("", "end", values=vals)

    

    def update_one(self):
        b = {self.edit_field.get(): self.edit_value.get()}
        r = self.client.update_biz_object(self.schema.get(), self.biz_id.get(), b)
        messagebox.showinfo("OK", json.dumps(r, ensure_ascii=False))

    def remove_one(self):
        r = self.client.remove_biz_object(self.schema.get(), self.biz_id.get())
        messagebox.showinfo("OK", json.dumps(r, ensure_ascii=False))

    def upload(self):
        files = []
        if self.file.get():
            files = [self.file.get()]
        elif self.dir.get():
            for p in ["*.png", "*.jpg"]:
                files += [str(x) for x in Path(self.dir.get()).glob(p)]
        items = []
        for f in files:
            items.append({"file": f, "result": self.client.upload_attachment(self.schema.get(), self.biz_id.get(), self.attach_field.get(), f)})
        messagebox.showinfo("OK", json.dumps({"ok": True, "count": len(items), "items": items}, ensure_ascii=False))

    def download(self):
        res = self.client.load_biz_object(self.schema.get(), self.biz_id.get())
        bo = (res.get("ReturnData") or {}).get("BizObject") or {}
        arr = bo.get(self.attach_field.get()) or []
        if isinstance(arr, str):
            arr = [arr]
        out_dir = self.out.get() or str(ROOT / "download" / self.attach_field.get())
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        items = []
        for aid in arr:
            items.append({"attachmentId": aid, "saved": self.client.download_attachment(aid, out_dir)})
        messagebox.showinfo("OK", json.dumps({"ok": True, "count": len(items), "out": out_dir, "items": items}, ensure_ascii=False))


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
