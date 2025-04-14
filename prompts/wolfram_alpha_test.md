<mcp>
name: wolfram-alpha-test
description: Ein Test-Prompt für den Wolfram Alpha MCP Server
arguments:
  - name: test_type
    description: Der Typ des Tests (math, science, conversion, formula)
    required: true
</mcp>

# Wolfram Alpha Test Prompt

Dieser Prompt demonstriert die Fähigkeiten des Wolfram Alpha MCP Servers. Der Server kann:

1. Mathematische Berechnungen durchführen
2. Wissenschaftliche Fragen beantworten
3. Datenanalysen durchführen
4. Einheiten umrechnen
5. Formeln lösen

## Test-Szenario

Bitte führe folgende Tests durch:

1. **Mathematische Berechnung**:
   - Berechne: 2 + 2
   - Berechne: 3 * 4
   - Berechne: 10 / 2

2. **Wissenschaftliche Frage**:
   - Was ist die Geschwindigkeit des Lichts?
   - Was ist die Masse der Erde?
   - Was ist die Temperatur der Sonne?

3. **Einheitenumrechnung**:
   - Konvertiere 100 Grad Celsius in Fahrenheit
   - Konvertiere 1 Kilometer in Meilen
   - Konvertiere 1 Kilogramm in Pfund

4. **Formel-Lösung**:
   - Löse die quadratische Gleichung: x^2 + 2x + 1 = 0
   - Berechne die Ableitung von x^2
   - Berechne das Integral von x^2

## Anweisungen

1. Verwende für jede Anfrage das `query`-Tool
2. Formuliere die Anfragen in natürlicher Sprache
3. Präsentiere die Ergebnisse klar und verständlich
4. Füge bei Bedarf Erklärungen hinzu

## Erwartetes Ergebnis

Der Server sollte:
- Alle Anfragen korrekt verarbeiten
- Klare und präzise Antworten liefern
- Bei Bedarf zusätzliche Informationen bereitstellen
- Fehler angemessen behandeln 