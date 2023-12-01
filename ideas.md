# miniplugins

TODO:
* jump by double click on struct field to function
* cphere() miniplugin который будет в буффер обмена копировать хекс от текущего адреса
* smart hexrays xrefs storage alt-x (to ints, to functions, to struct member fields)
* F1 hotkey to ask LLama what current function does
* Ф2 хоткей в иде про для переименования всего подряд
* ida F3 hotkey: get xrefs to current function in HR window from anywhere. взять функу, найти все её вызовы по хрефам, для каждого вызова найти то, как она вызывается и вывести (удобно аргументы смотреть). аналог XrefStorage'a потому что надо декомпилировать много функций и сохранять результат использования
* miniplugin, который на загрузке идбхи сортирует окно функций
* plugin, that creates default folders for functions and for structures (c++ funcs, for libraries imports)
* vim mode ida pro: G gg H L h j k l a w b A
* strip ida generated name to default form 'v" + str(lvar_id)
* easier enum usage. действие добавление имени константе через создание енама с одним единственным числом. действие добавление константы к уже существующему енаму
* плагин, который отрубает нахуй меню сверху, которое регулярно на альт триггерится
* плагин, который по хоткею справа слева будет окошко с функциями показывать/прятать. такой же плагин для окошка со структурами по хоткею справа
