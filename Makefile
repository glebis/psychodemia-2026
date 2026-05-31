# Демо мастер-класса. Запускайте: make demo
.PHONY: demo demo-1 demo-2 demo-3 refs
demo:
	@echo "Паттерны в массиве сессий — демо"
	@echo "  make demo-1   # Можно ли убрать идентификаторы? (анонимизация + ручная проверка)"
	@echo "  make demo-2   # Может ли модель обосновать искажение цитатами? (DoT, одна сессия)"
	@echo "  make demo-3   # Виден ли повторяющийся паттерн через 5 сессий? (тренд)"
	@echo "  make refs     # Открыть эталонные результаты (страховка)"
demo-1:
	@echo '>>> Открой prompts/PROMPTS.md → промпт 1, запусти на sessions-ru/client-a/session-01.md'
	@echo '>>> Затем промпт 2 (квази-идентификаторы). Эталон: reference-outputs/01-anonymization.md'
demo-2:
	@echo '>>> prompts/PROMPTS.md → промпт 3 (DoT). Эталон: reference-outputs/03-dot-analysis.md'
demo-3:
	@echo '>>> prompts/PROMPTS.md → промпт 5 (тренд). Эталон: reference-outputs/05-multisession-trend.md'
refs:
	@ls -1 reference-outputs/
