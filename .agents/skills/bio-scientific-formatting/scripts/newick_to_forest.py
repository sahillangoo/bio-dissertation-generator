#!/usr/bin/env python3
"""
newick_to_forest.py - Converts Newick Phylogenetic Trees into LaTeX TikZ/Forest Code

Parses standard Newick tree strings (with taxon labels, bootstrap support,
and branch lengths) and emits clean LaTeX TikZ/Forest code for crisp vector rendering.
"""

import argparse
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Tuple


class TreeNode:
    def __init__(self, label: str = "", length: Optional[float] = None, support: Optional[str] = None):
        self.label = label.strip()
        self.length = length
        self.support = support
        self.children: List['TreeNode'] = []

    def is_leaf(self) -> bool:
        return len(self.children) == 0


def parse_newick_tokens(newick_str: str) -> List[str]:
    """Tokenize Newick string into parentheses, commas, colons, semicolons, and words."""
    # Strip whitespace and trailing semicolon
    s = newick_str.strip()
    if s.endswith(";"):
        s = s[:-1].strip()

    tokens = []
    curr = []
    i = 0
    while i < len(s):
        c = s[i]
        if c in "(),:;":
            if curr:
                tokens.append("".join(curr).strip())
                curr = []
            tokens.append(c)
        elif c.isspace():
            if curr:
                tokens.append("".join(curr).strip())
                curr = []
        else:
            curr.append(c)
        i += 1
    if curr:
        tokens.append("".join(curr).strip())
    return [t for t in tokens if t]


def parse_newick(tokens: List[str]) -> TreeNode:
    """Parse token list into a TreeNode tree."""
    idx = 0

    def parse_subtree() -> TreeNode:
        nonlocal idx
        node = TreeNode()
        if idx < len(tokens) and tokens[idx] == "(":
            idx += 1  # consume '('
            while idx < len(tokens):
                child = parse_subtree()
                node.children.append(child)
                if idx < len(tokens) and tokens[idx] == ",":
                    idx += 1
                elif idx < len(tokens) and tokens[idx] == ")":
                    idx += 1
                    break
                else:
                    break

        # After ')' or if leaf, token may be label / support
        if idx < len(tokens) and tokens[idx] not in "(),:":
            val = tokens[idx]
            idx += 1
            if node.is_leaf():
                node.label = val
            else:
                node.support = val

        # Check for branch length
        if idx < len(tokens) and tokens[idx] == ":":
            idx += 1  # consume ':'
            if idx < len(tokens) and tokens[idx] not in "(),:":
                try:
                    node.length = float(tokens[idx])
                except ValueError:
                    pass
                idx += 1

        return node

    return parse_subtree()


def clean_taxon_name(raw_name: str) -> str:
    """Format taxon label for LaTeX (convert underscores to spaces, italicize)."""
    clean = raw_name.replace("_", " ").strip()
    if not clean:
        return ""
    # If standard binomial, italicize
    parts = clean.split()
    if len(parts) >= 2 and parts[0][0].isupper() and parts[1].islower():
        return f"\\textit{{{clean}}}"
    return clean


def node_to_forest(node: TreeNode, indent_level: int = 1) -> str:
    """Recursively convert TreeNode to Forest syntax."""
    indent = "  " * indent_level

    if node.is_leaf():
        taxon = clean_taxon_name(node.label)
        return f"{indent}[{taxon}]"

    # Interior node
    child_lines = [node_to_forest(ch, indent_level + 1) for ch in node.children]
    joined_children = "\n".join(child_lines)

    node_options = ""
    if node.support:
        # Render bootstrap / posterior probability above or below branch
        node_options = f", edge label={{node[midway, below]{{\\tiny {node.support}}}}}"

    return f"{indent}[{node_options}\n{joined_children}\n{indent}]"


def generate_forest_latex(root: TreeNode, caption: str = "Phylogenetic tree reconstructed from concatenated sequences.", label: str = "fig:phylogeny_tree") -> str:
    """Generate complete LaTeX figure environment containing forest tree."""
    tree_content = node_to_forest(root, indent_level=2)

    latex_code = f"""\\begin{{figure}}[htbp]
\\centering
\\begin{{forest}}
  for tree={{
    grow'=0,
    forked edges,
    font=\\small,
    draw,
    rounded corners,
    edge={{draw=black, thick}},
    parent anchor=east,
    child anchor=west,
    l=1.5cm,
    s sep=0.8cm
  }}
{tree_content}
\\end{{forest}}
\\caption{{{caption}}}
\\label{{{label}}}
\\end{{figure}}
"""
    return latex_code


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert Newick phylogenetic tree format to LaTeX TikZ/Forest code."
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        help="Input file containing Newick tree string",
    )
    parser.add_argument(
        "--newick",
        "-n",
        type=str,
        help="Direct Newick tree string (e.g. '((A,B)95,C);')",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output file path for generated LaTeX code (prints to stdout if omitted)",
    )
    parser.add_argument(
        "--caption",
        "-c",
        type=str,
        default="Phylogenetic relationship of sampled taxa inferred using Maximum Likelihood.",
        help="Figure caption for LaTeX output",
    )
    parser.add_argument(
        "--label",
        "-l",
        type=str,
        default="fig:phylogeny_tree",
        help="Figure label for LaTeX cross-referencing",
    )

    args = parser.parse_args()

    newick_text = ""
    if args.input:
        newick_text = args.input.read_text(encoding="utf-8").strip()
    elif args.newick:
        newick_text = args.newick.strip()
    else:
        # Default sample if nothing provided
        newick_text = "((Sceloporus_occidentalis:0.04,Sceloporus_graciosus:0.05)98:0.03,Uta_stansburiana:0.09);"

    tokens = parse_newick_tokens(newick_text)
    if not tokens:
        sys.stderr.write("Error: Could not parse Newick tokens.\n")
        return 1

    root = parse_newick(tokens)
    latex_output = generate_forest_latex(root, caption=args.caption, label=args.label)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(latex_output, encoding="utf-8")
        print(f"Forest LaTeX code saved to {args.output}")
    else:
        print(latex_output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
