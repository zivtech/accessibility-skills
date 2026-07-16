#!/usr/bin/env python3
"""Render a11y-critic eval fixtures (React/JSX in markdown) into live HTML pages
so keyboard-a11y-tester can be cross-validated against known planted bugs."""
import re
import sys
from pathlib import Path

FIXTURES = Path("/Users/AlexUA_1/claude/a11y-meta-skills/evals/suites/a11y-critic/fixtures")
OUT = Path(__file__).parent / "pages"
OUT.mkdir(parents=True, exist_ok=True)

# Per-fixture render expressions. Default is <Component />.
SHIMS = {
    "accordion-no-region-role": "<BuggyAccordion items={[{title:'Shipping policy',content:'We ship worldwide within 5 business days.'},{title:'Returns',content:'30-day return window on all items.'},{title:'Warranty',content:'One-year limited warranty.'}]} />",
    "breadcrumb-navigation-no-nav-landmark": "<BuggyBreadcrumb items={[{label:'Home',href:'#/'},{label:'Products',href:'#/products'},{label:'Laptops',href:'#/products/laptops',current:true}]} />",
    "button-skip-link-clean": "<MainLayout><h2>Latest articles</h2><p>Body content for the layout fixture.</p></MainLayout>",
    "checkbox-group-no-fieldset": "<BuggyCheckboxGroup label='Pizza toppings' options={['Cheese','Mushrooms','Peppers']} />",
    "combobox-autocomplete-no-listbox-role": "<BuggyCombobox label='Country' options={['Canada','Chile','China','Colombia']} />",
    "expandable-section-no-button": "<BuggyExpandable title='Shipping details' content='Orders ship within 2 business days.' />",
    "image-carousel-no-region": "<BuggyCarousel images={[{src:'red-bike.jpg',alt:'Red bicycle'},{src:'blue-helmet.jpg',alt:'Blue helmet'},{src:'lock.jpg'}]} />",
    "interactive-dropdown-clean": "<DropdownSelect label='Sort by' options={['Newest','Price: low to high','Rating']} onSelect={()=>{}} />",
    "interactive-dropdown-focus-bug": "<BuggyDropdown label='Sort by' options={['Newest','Price: low to high','Rating']} onSelect={()=>{}} />",
    "megamenu-no-structure": "<BuggyMegaMenu items={[{label:'Products',children:[{label:'Laptops',href:'#laptops'},{label:'Phones',href:'#phones'}]},{label:'Support',children:[{label:'Contact us',href:'#contact'}]}]} />",
    "modal-complete-clean": None,  # needs stateful wrapper, see WRAPPERS
    "pagination-no-nav-landmark": "<BuggyPagination currentPage={3} totalPages={10} onPageChange={()=>{}} />",
    "popover-no-focus-management": "<BuggyPopover trigger='More info' content='Popovers provide supplemental details about a control.' />",
    "radio-button-group-no-grouping": "<BuggyRadioGroup label='Subscription plan' options={['Basic','Pro','Enterprise']} />",
    "search-focus-stays-in-input": "<LiveSearch onSearch={()=>{}} />",
    "tabs-incomplete-aria-selected": "<ProductTabs products={[{id:1,name:'Laptops',description:'Portable computers',count:2,items:[{id:11,title:'AeroBook 13',price:'$999',url:'#a13'},{id:12,title:'AeroBook 15',price:'$1299',url:'#a15'}]},{id:2,name:'Phones',description:'Smartphones',count:1,items:[{id:21,title:'Pixel 9',price:'$799',url:'#p9'}]}]} />",
    "tabs-missing-arrow-nav": "<TabsWidget tabs={[{id:'overview',label:'Overview',content:'Overview body text.'},{id:'specs',label:'Specifications',content:'Specification body text.'},{id:'reviews',label:'Reviews',content:'Review body text.'}]} />",
    "toast-notification-no-role": "<BuggyToast message='Profile saved successfully' duration={600000} />",
    "tooltip-no-role-no-association": "<BuggyTooltip trigger='Delete item' content='Permanently removes the item from your library.' />",
    "video-player-missing-captions": "<BuggyVideoPlayer videoSrc='sample.mp4' />",
}

WRAPPERS = {
    "tabbed-nav-vs-tab-pattern": """
// Next.js router stub: hash-based so route changes are observable without Next.
const useRouter = () => ({ push: (p) => { window.location.hash = p; } });
const usePathname = () => (window.location.hash || '#/overview').replace('#', '');
""",
    "modal-complete-clean": """
const Demo = () => {
  const [open, setOpen] = useState(false);
  return (
    <div>
      <button onClick={() => setOpen(true)}>Open settings</button>
      <Modal isOpen={open} onClose={() => setOpen(false)} title="Settings">
        <p>Notification preferences for your account.</p>
        <button onClick={() => setOpen(false)}>Save changes</button>
      </Modal>
    </div>
  );
};
""",
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{fid}</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 16px; }}
{css}
</style>
</head>
<body>
<div id="root"></div>
<script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script type="text/babel">
const {{ useState, useEffect, useRef, useCallback, useMemo, useId, useLayoutEffect, Fragment }} = React;
{code}
{wrapper}
ReactDOM.createRoot(document.getElementById('root')).render({render});
</script>
</body>
</html>
"""


def extract_blocks(md_text, lang):
    return re.findall(r"```" + lang + r"\n(.*?)```", md_text, re.DOTALL)


def transform(code):
    code = re.sub(r"^import .*?;\s*$", "", code, flags=re.MULTILINE)
    code = re.sub(r"^import .*?$", "", code, flags=re.MULTILINE)
    code = re.sub(r"^export default (\w+);?\s*$", "", code, flags=re.MULTILINE)
    code = re.sub(r"^export ", "", code, flags=re.MULTILINE)
    return code


def main():
    built, skipped = [], []
    for md in sorted(FIXTURES.glob("*.md")):
        fid = md.stem
        text = md.read_text()
        jsx = extract_blocks(text, "jsx") + extract_blocks(text, "javascript")
        css = extract_blocks(text, "css")
        if not jsx:
            skipped.append((fid, "no jsx block"))
            continue
        exp = re.search(r"export default (\w+)", "\n".join(jsx))
        if not exp:
            skipped.append((fid, "no default export"))
            continue
        name = exp.group(1)
        code = "\n".join(transform(b) for b in jsx)
        wrapper = WRAPPERS.get(fid, "")
        if "const Demo" in wrapper:
            render = "<Demo />"
        else:
            render = SHIMS.get(fid) or f"<{name} />"
        html = TEMPLATE.format(fid=fid, css="\n".join(css), code=code, wrapper=wrapper, render=render)
        (OUT / f"{fid}.html").write_text(html)
        built.append(fid)
    print(f"built {len(built)} pages -> {OUT}")
    for fid, why in skipped:
        print(f"SKIPPED {fid}: {why}", file=sys.stderr)


if __name__ == "__main__":
    main()
