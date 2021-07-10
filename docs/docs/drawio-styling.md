# DrawIO Styling

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Diagraming tools](#diagraming-tools)
- [Style guide](#style-guide)
- [The easy way to apply the styling](#the-easy-way-to-apply-the-styling)

<!-- mdformat-toc end -->

## Diagraming tools<a name="diagraming-tools"></a>

- [draw.io](https://app.diagrams.net/)
- [VSCode DrawIO extension (`hediet.vscode-drawio`)](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio)

## Style guide<a name="style-guide"></a>

- line color: `#FF8000`

- line style: `sketch`

- text color: `#6EA31D`

- text background: None

- text border: None

- shape fill opacity: 0

- keep diagrams to a single landscape A4 page

- don't create multi-page `.drawio` diagrams, instead create multiple drawIO diagrams (eg.
  `git-guide.drawio`, `git-guide-1.drawio`, `git-guide-2.drawio`, ...)

## The easy way to apply the styling<a name="the-easy-way-to-apply-the-styling"></a>

1. Complete you diagram

2. Select everything (ctrl+A)

3. Set line details

   ![setting line details](../images/exports/docs/drawio-styling/line-details.jpg)

4. Remove the excess box-borders (all text on arrows will have borders at this point)

5. Set text details

   ![setting text details](../images/exports/docs/drawio-styling/text-details.jpg)

6. Set fill opacity to `0` under the "style" tab

   ![setting fill opacity to zero](../images/exports/docs/drawio-styling/fill-opacity.jpg)

7. Edits will apply to everything selected so this way you won't have to edit each shape
   individually
